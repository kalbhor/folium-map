import folium
import requests
import json
import key

search = input("Enter the Location ");

url = 'https://developers.zomato.com/api/v2.1/categories'
headers = {'user-key': key.key}
r = requests.get(url, headers=headers)
categories=r.json();

url= 'https://developers.zomato.com/api/v2.1/locations?query=' + search.replace(" ", "%20");
r = requests.get(url, headers=headers)
location = r.json();
fg=[];
index=0;
url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + search.replace(" ", "%20");
r = requests.get(url);
geo = r.json();
map=folium.Map(location=[geo['results'][0]['geometry']['location']['lat'],geo['results'][0]['geometry']['location']['lng']],zoom_start=16);
for i in categories['categories']:
    fg.append(folium.FeatureGroup(name=i['categories']['name']))
    for l in location['location_suggestions']:
        url = 'https://developers.zomato.com/api/v2.1/search?entity_id=' +str(l['entity_id']) + '&entity_type=' +l['entity_type'] + '&category=' + str(i['categories']['id']);
        r = requests.get(url, headers=headers);
        rest = r.json();
        for loc in rest['restaurants']:
            fg[index].add_child(folium.Marker(location=[loc['restaurant']['location']['latitude'],loc['restaurant']['location']['longitude']], popup=loc['restaurant']['name'], icon=folium.Icon(color='red')));
    map.add_child(fg[index]);
    index=index+1;


map.add_child(folium.LayerControl());
map.save("./rendered_html/Map1.html");
