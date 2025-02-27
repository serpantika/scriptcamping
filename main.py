import json
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="uvcamping"
)
j = 0
newdata= {}
def load_json_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the file.")
        return None

def save_json_to_bdd(data):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO campings(user_id, name, address, city, postal_code, phone, email, website, description, latitude, longitude, price, stars) 
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                       (data.get('user_id', ''), data.get('name', ''), data.get('address', ''), data.get('city', ''),
                        data.get('postal_code', ''), data.get('phone', ''), data.get('email', ''),
                        data.get('website', ''),
                        data.get('description', ''), data.get('latitude', ''), data.get('longitude', ''),
                        data.get('price', ''), data.get('stars', '')))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
def transform_json(data):
    if data is not None:
        print(data[1])
        print(data[1]['type'])
    for index in range (len(data)):
        if data[index]['type'] == 'camp_site' or data[index]['type'] == 'caravan_site' or data[index]['type'] == 'wilderness_hut' or data[index]['type'] == 'alpine_hut' :
            newdata['user_id'] = ''
            newdata['name']=data[index]['name']
            newdata['address'] = data[index]['meta_name_dep']
            newdata['city'] = data[index]['meta_name_com']
            newdata['postal_code'] = data[index]['meta_code_com']
            newdata['phone'] = data[index]['phone']
            newdata['email'] = data[index]['email']
            newdata['website'] = data[index]['website']
            newdata['description'] = ''
            newdata['latitude'] = data[index]['meta_geo_point']['lat']
            newdata['longitude'] = data[index]['meta_geo_point']['lon']
            newdata['price'] = ''
            newdata['stars'] = data[index]['stars']
            save_json_to_bdd(newdata)
        else:
            print('pas adéquat')

if __name__ == "__main__":
    file_path = r"C:\Users\Afpa\Downloads\osm-france-tourism-accommodation.json"
    json_data = load_json_from_file(file_path)
    transform_json(json_data)
