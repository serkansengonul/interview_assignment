from flask import Flask, request, jsonify
import psycopg2
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

"""
This module provides a Flask web service to retrieve the top 5 sellers based on Gross Merchandise Value (GMV) for a given category. 
It connects to a PostgreSQL database to fetch this data.

Functions:
    calculate_gmv(category_id): Calculates GMV for the given category and returns the top 5 sellers.
    top_sellers(): Flask endpoint to retrieve the top 5 sellers for a given category.
"""

app = Flask(__name__)


def calculate_gmv(category_id):
    """
    Calculate the Gross Merchandise Value (GMV) for sellers in the given category.

    Parameters:
        category_id (str): The ID of the category to filter sellers.

    Returns:
        list: A list of tuples containing seller IDs and their respective GMV.
    """
    conn = psycopg2.connect(
        dbname="n11db",
        user="user",
        password="password",
        host="db",
        port="5432"
    )

    cur = conn.cursor()

    # SQL query to calculate GMV
    sql = """
    SELECT s.sellerid, SUM(o.price) AS GMV
    FROM sellers s
    JOIN orders o ON o.sellerids LIKE '%' || s.sellerid || '%'
    WHERE s.categoryid = '{}' AND o.orderstatus = 'SUCCESS'
    GROUP BY s.sellerid
    ORDER BY GMV DESC
    LIMIT 5;
    """.format(category_id)

    try:
        cur.execute(sql)
        result = cur.fetchall()
        logging.info(f"GMV calculated for category ID: {category_id}")
    except Exception as e:
        logging.error(f"Error calculating GMV for category ID {category_id}: {e}")
        raise

    cur.close()
    conn.close()

    return result


@app.route('/top_sellers', methods=['GET'])
def top_sellers():
    """
    Flask endpoint to retrieve the top 5 sellers based on GMV for a given category.

    Query Parameters:
        cat (str): The category ID to filter sellers.

    Returns:
        json: A JSON list of top 5 seller IDs for the given category.
    """
    category_id = request.args.get('cat')
    gmv_result = calculate_gmv(category_id)
    sellers = [row[0] for row in gmv_result]
    logging.info(f"Top sellers retrieved for category ID: {category_id}")
    return jsonify(sellers)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1234)
