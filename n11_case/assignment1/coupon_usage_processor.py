import coupon_data_processor


class CouponUsageProcessor(coupon_data_processor.CouponDataProcessor):  # Inherits from our previous class
    """
    The CouponUsageProcessor class inherits from CouponDataProcessor.
    It focuses on processing coupon usage related data and saving it to BigQuery.
    """

    def calculate_used_coupons(self):
        """
        Calculate the number of coupons used for each category, year, and month.
        """
        query = """
        SELECT 
            EXTRACT(YEAR FROM kullanim_tarihi) as year,
            EXTRACT(MONTH FROM kullanim_tarihi) as month,
            ana_kategori_adi2,
            COUNT(DISTINCT kupon_kullanim_id) as kullanilan_kupon_sayisi
        FROM `n11-DEDS-veri.n11_VA_tablolari.Kupon_Kullanim`
        JOIN `n11-DEDS-veri.n11_VA_tablolari.Kategori_Cizelge` 
        ON Kupon_Kullanim.kupon_id = Kategori_Cizelge.kategori_id
        GROUP BY year, month, ana_kategori_adi2
        """
        return self.fetch_data(query)

    def calculate_GMV(self):
        """
        Calculate the Gross Merchandise Volume (GMV) for each category, year, and month.
        """
        query = """
        SELECT 
            EXTRACT(YEAR FROM kullanim_tarihi) as year,
            EXTRACT(MONTH FROM kullanim_tarihi) as month,
            ana_kategori_adi2,
            SUM(fiyat * adet) as GMV
        FROM `n11-DEDS-veri.n11_VA_tablolari.Kupon_Kullanim`
        JOIN `n11-DEDS-veri.n11_VA_tablolari.Siparis_Kalemleri` 
        ON Kupon_Kullanim.siparis_id = Siparis_Kalemleri.siparis_id
        JOIN `n11-DEDS-veri.n11_VA_tablolari.Kategori_Cizelge` 
        ON Siparis_Kalemleri.urun_id = Kategori_Cizelge.kategori_id
        GROUP BY year, month, ana_kategori_adi2
        """
        return self.fetch_data(query)

    def calculate_total_discount(self):
        """
        Calculate the total discount given for each category, year, and month.
        """
        query = """
        SELECT 
            EXTRACT(YEAR FROM kullanim_tarihi) as year,
            EXTRACT(MONTH FROM kullanim_tarihi) as month,
            ana_kategori_adi2,
            SUM(
                CASE 
                    WHEN indirim_tipi = 'oran' THEN (indirim_miktari / 100) * fiyat
                    WHEN indirim_tipi = 'miktar' THEN indirim_miktari
                    ELSE 0
                END
            ) as toplam_indirim
        FROM `n11-DEDS-veri.n11_VA_tablolari.Kupon_Kullanim`
        JOIN `n11-DEDS-veri.n11_VA_tablolari.Kuponlar` 
        ON Kupon_Kullanim.kupon_id = Kuponlar.kupon_id
        JOIN `n11-DEDS-veri.n11_VA_tablolari.Siparis_Kalemleri` 
        ON Kupon_Kullanim.siparis_id = Siparis_Kalemleri.siparis_id
        JOIN `n11-DEDS-veri.n11_VA_tablolari.Kategori_Cizelge` 
        ON Siparis_Kalemleri.urun_id = Kategori_Cizelge.kategori_id
        GROUP BY year, month, ana_kategori_adi2
        """
        return self.fetch_data(query)

    def construct_coupon_usage_table(self):
        """
        Construct the Kupon_Kullanim table by merging various datasets.
        This table includes metrics like the number of used coupons, GMV, and total discount.
        """
        used_coupons_data = self.calculate_used_coupons()
        GMV_data = self.calculate_GMV()
        total_discount_data = self.calculate_total_discount()

        merged_data = used_coupons_data.merge(GMV_data, on=['year', 'month', 'ana_kategori_adi2'], how='left')
        merged_data = merged_data.merge(total_discount_data, on=['year', 'month', 'ana_kategori_adi2'], how='left')

        return merged_data[['year', 'month', 'ana_kategori_adi2', 'kullanilan_kupon_sayisi', 'GMV', 'toplam_indirim']]


if __name__ == "__main__":
    """
    The entry point of the script.
    Initializes the CouponUsageProcessor, constructs the Kupon_Kullanim table, 
    and saves it to BigQuery.
    """
    SERVICE_ACCOUNT_JSON = 'YOUR_SERVICE_ACCOUNT_JSON'
    PROJECT_ID = 'YOUR_PROJECT_ID'
    DATASET_NAME = 'n11_VA_tablolari'
    TABLE_NAME = 'Kupon_Kullanim'

    processor = CouponUsageProcessor(SERVICE_ACCOUNT_JSON, PROJECT_ID, DATASET_NAME, TABLE_NAME)
    coupon_usage_table = processor.construct_coupon_usage_table()
    processor.save_to_bigquery(coupon_usage_table)
    print(f"Saved the data to {DATASET_NAME}.Kupon_Kullanim in BigQuery!")
