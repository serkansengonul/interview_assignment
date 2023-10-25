from google.cloud import bigquery
from google.oauth2 import service_account


class CouponDataProcessor:
    def __init__(self, service_account_json, project_id, dataset_name, table_name):
        """
        Initialize the CouponDataProcessor object with necessary credentials and configurations.
        Set up a BigQuery client for further operations.
        """
        self.credentials = service_account.Credentials.from_service_account_file(service_account_json)
        self.client = bigquery.Client(credentials=self.credentials, project=project_id)
        self.dataset_name = dataset_name
        self.table_name = table_name

    def fetch_data(self, query):
        """
        Execute the given SQL query against BigQuery and return the results as a DataFrame.
        """
        return self.client.query(query).to_dataframe()

    def get_year_month(self):
        """
        Extract distinct Year and Month values from the coupon's validity start date.
        """
        query = """
        SELECT DISTINCT 
            EXTRACT(YEAR FROM gecerlilik_baslangic_tarihi) as year,
            EXTRACT(MONTH FROM gecerlilik_baslangic_tarihi) as month
        FROM `n11-DEDS-veri.n11_VA_tablolari.Kuponlar`
        """
        return self.fetch_data(query)

    def get_categories(self):
        """
        Extract distinct category names from the Kategori_Cizelge table.
        """
        query = """
        SELECT DISTINCT ana_kategori_adi2 
        FROM `n11-DEDS-veri.n11_VA_tablolari.Kategori_Cizelge`
        """
        return self.fetch_data(query)

    def get_available_coupons(self):
        """
        Count available coupons for a specific year and month.
        """
        query = """
        SELECT 
            EXTRACT(YEAR FROM gecerlilik_baslangic_tarihi) as year,
            EXTRACT(MONTH FROM gecerlilik_baslangic_tarihi) as month,
            COUNT(kupon_id) as kullanilabilir_kupon_sayisi
        FROM `n11-DEDS-veri.n11_VA_tablolari.Kuponlar`
        GROUP BY year, month
        """
        return self.fetch_data(query)

    def calculate_potential_coupon_cost(self):
        """
        Calculate the potential cost for each coupon.
        """
        query = """
        SELECT 
            kupon_id,
            CASE 
                WHEN indirim_tipi = 'oran' THEN (indirim_miktari / 100) * fiyat
                WHEN indirim_tipi = 'miktar' THEN indirim_miktari
                ELSE 0
            END as potansiyel_kupon_maliyeti
        FROM `n11-DEDS-veri.n11_VA_tablolari.Kuponlar` 
        JOIN `n11-DEDS-veri.n11_VA_tablolari.Urun` 
        ON Kuponlar.kupon_id = Urun.urun_id
        """
        return self.fetch_data(query)

    def calculate_potential_GMV(self):
        """
        Calculate the potential GMV if all coupons were used.
        """
        query = """
        SELECT 
            kupon_id,
            SUM(fiyat) as olusacak_GMV
        FROM `n11-DEDS-veri.n11_VA_tablolari.Kuponlar` 
        JOIN `n11-DEDS-veri.n11_VA_tablolari.Siparis_Kalemleri` 
        ON Kuponlar.kupon_id = Siparis_Kalemleri.urun_id
        GROUP BY kupon_id
        """
        return self.fetch_data(query)

    def construct_potential_coupon_cost_table(self):
        """
        Construct the Potansiyel_Kupon_Maliyeti table by merging various datasets.
        This table includes potential coupon costs, GMV, and other related metrics.
        """
        year_month_data = self.get_year_month()
        category_data = self.get_categories()
        available_coupons_data = self.get_available_coupons()
        potential_coupon_cost_data = self.calculate_potential_coupon_cost()
        potential_GMV_data = self.calculate_potential_GMV()

        merged_data = year_month_data.merge(category_data, how='cross')
        merged_data = merged_data.merge(available_coupons_data, on=['year', 'month'], how='left')
        merged_data = merged_data.merge(potential_coupon_cost_data, on='kupon_id', how='left')
        merged_data = merged_data.merge(potential_GMV_data, on='kupon_id', how='left')

        return merged_data[
            ['year', 'month', 'ana_kategori_adi2', 'kullanilabilir_kupon_sayisi', 'potansiyel_kupon_maliyeti',
             'olusacak_GMV']]

    def save_to_bigquery(self, dataframe):
        """
        Save the provided dataframe to BigQuery with the specified dataset and table names.
        """
        dataset_ref = self.client.dataset(self.dataset_name)
        table_ref = dataset_ref.table(self.table_name)
        job_config = bigquery.LoadJobConfig()
        job_config.autodetect = True
        job_config.write_disposition = "WRITE_TRUNCATE"  # This will overwrite the existing table
        load_job = self.client.load_table_from_dataframe(dataframe, table_ref, job_config=job_config)
        load_job.result()


if __name__ == "__main__":
    """
    The entry point of the script.
    Initializes the CouponDataProcessor, constructs the Potansiyel_Kupon_Maliyeti table, 
    and saves it to BigQuery.
    """
    SERVICE_ACCOUNT_JSON = 'YOUR_SERVICE_ACCOUNT_JSON'
    PROJECT_ID = 'YOUR_PROJECT_ID'
    DATASET_NAME = 'n11_VA_tablolari'
    TABLE_NAME = 'Potansiyel_Kupon_Maliyeti'

    processor = CouponDataProcessor(SERVICE_ACCOUNT_JSON, PROJECT_ID, DATASET_NAME, TABLE_NAME)
    potential_coupon_cost_table = processor.construct_potential_coupon_cost_table()
    processor.save_to_bigquery(potential_coupon_cost_table)
    print(f"Saved the data to {DATASET_NAME}.{TABLE_NAME} in BigQuery!")
