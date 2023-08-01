# Data Model Description

This data model describes a single feature in Ausome Maps, representing a therapy center for differently-abled individuals. The feature has both geometric and property information. Below is the breakdown of each part of the data model:

1. **id**
   Unique identifier for this entry/feature/row.

2. **geometry**

   - **type (Point)**
   
      The type of the feature, which is "Point" in this case, indicating that the data represents a geographic point location.

   - **coordinates (LatLng)**
  
     Contains the geographical coordinates (longitude, latitude, and altitude) of the therapy center, represented as a "Point" type.

     ```
      "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    121.545819,
                    16.682762
                ]
     ```

3. **properties**

   This section includes various properties of the therapy center:

   - **date_updated (DateTime)**

     The date and time of the feature entry or last updated (in the format "YYYY-MM-DDTHH:mm:ss.sss+08:00").
     ```
      "properties": {
                 ...
                "date_updated": "2023-07-05T21:47:19.651+08:00",
                 ...
     }
     ```

   - **osmid (String)**
     ID of the OSM feature that corresponds to this entry. 

   - **info_src_name (String)**

     Name of the information source. ("Garry Louie Sabado" in this case)
      ```
      "properties": {
                 ...
                "info_src_name": "Last name, First name",
                 ...
     }
     ```

   - **info_src_designation (String)**

     Designation/role of the information source.
     ```
      "properties": {
                 ...
                "info_src_designation": "Managing Director",
                 ...
     }
     ```

   - **placename (String)**
     Name of the therapy center or official business name as registered. 
     ```
      "properties": {
                 ...
                "placename": "Placename Intervention Therapy Center",
                 ...
     }
     ```
     
   - **desc_long (String)**
     A 2-3 sentence paragraph writeup about the therapy center
     ```
      "properties": {
                 ...
                "desc_long": "At Blausome Therapy Center, we are dedicated to providing exceptional care and support for individuals with diverse abilities. Nestled in the heart of Santiago City, Isabela, our center serves as a haven for pediatric, adolescent, and adult populations seeking specialized therapy services.",
                 ...
     }
     ```
   - **desc_short (String)**
     One-liner/tag line of your therapy center
     ```
      "properties": {
                 ...
                "desc_short": "Together Towards a Brighter Tomorrow",
                 ...
     }
     ```

   - **address (String)**
     Physical address of the therapy center. Complete business address.
     ```
      "properties": {
                 ...
                "address": "20 Pangustura St., Midtown Subd. Ph-3, San Roque, Marikina City, Metro Manila, 1801",
                 ...
     }
     ```

   - **region (String)**
     Region where the therapy center is located.
     ```
      "properties": {
                 ...
                "region": "NCR – National Capital Region",
                 ...
     }
     ```

   - **city_province (String)**
     City or province where the therapy center is situated.
      ```
      "properties": {
                 ...
                "city_province": "Marikina City",
                 ...
     }
     ```

   - **landmarks_desc (String)**
     Description of nearby landmarks.
     ```
      "properties": {
                 ...
                "landmarks_desc": "Right beside 45th Studio Hotel",
                 ...
     }
     ```

   - **contact_number_mobile (String)**
     Primary mobile contact number of the therapy center.
     ```
      "properties": {
                 ...
                "contact_number_mobile": "+63XXXXXXXXXX",
                 ...
     }
     ```
   - **contact_number_landline (String)**
     Primary landline contact number of the therapy center.
     ```
      "properties": {
                 ...
                "contact_number_landline": "02-XXXX-XXXX",
                 ...
     }
     ```

   - **alt_contact_numbers (String)**
     Alternative contact numbers separated by commas.
     ```
      "properties": {
                 ...
                "alt_contact_numbers": "alt_contact_1, alt_contact_2, alt_contact_3",
                 ...
     }
     ```

   - **email_address (String)**
     Email address of the therapy center.
     ```
      "properties": {
                 ...
                "email_address": "emailadd@domain.com",
                 ...
     }
     ```

   - **website (String)**
     Website URL of the therapy center. Must be a working link to the website.
     ```
      "properties": {
                 ...
                "website": "https://ausomemaps.org",
                 ...
     }
     ```

   - **social_media (Object)**
     Social media accounts available/owned by the therapy center/school.

        *facebook* - Indicates if the therapy center has a presence on Facebook. Must be a working facebook page or account url.
     
        *instagram* - Indicates if the therapy center has a presence on Instagram. Must be the Instagram handle of the therapy center or school.

     ```
      "properties": {
                 ...
                "social_media": {
                    "facebook":"https://www.facebook.com/ausomemaps/",
                    "instagram": "ausomemapsph",
                    },
                 ...
     }
     ```

   - **caters_to (Array)**
     Describes the target populations the therapy center caters to.
     ```
      "properties": {
                 ...
                "caters_to": ['Pediatric','Adolescent','Adult'],
                 ...
     }
     ```

   - **services_offered**
     The following attributes indicate the types of services offered by the therapy center, specifying whether they are provided to individuals, groups, or through teletherapy, as well as home service options.
                   
      | Session Type         | Indicator |
      |----------------------|-----------|
      | No Offering          | 0         |
      | Individual           | 1         |
      | Group                | 2         |
      | Individual and Group | 3         |

      | Key                     | Label                           |
      |-------------------------|---------------------------------|
      | speechlanguagetherapy   | Speech-Language Therapy         |
      | speechlanguagepathology | Speech-Language Pathology       |
      | occupationaltherapy     | Occupational Therapy            |
      | behavioraltherapy       | Behavioral Therapy              |
      | physicaltherapy         | Physical Therapy                |
      | lifeskillstraining      | Life Skills Training            |
      | socialskillstraining    | Social Skills Training          |
      | integration             | Integration                     |
      | integrationprogram      | Integration Program             |
      | jobcoaching             | Job Coaching                    |
      | specialeducation        | Special Education               |
      | spedtutorials           | SpEd Tutorials                  |
      | parentcoaching          | Parent Coaching                 |
      | educationsessionforfamilies | Education Session for Families |
      | feeding                 | Feeding                         |
      | counseling              | Counseling                      |
      | psychotherapy           | Psychotherapy                   |
      | abatherapy              | ABA Therapy                     |
      | mnri                    | MNRI                            |
      | sensoryintegration      | Sensory Integration             |
      | playschool              | Play School                     |
      | dysphagiamanagement     | Dysphagia Management            |
      | orthoses                | Orthoses (Splinting)            |

     ```
      "properties": {
                 ...
                "services_offered": {
                  'service_1':{
                             'teletherapy':0,
                             'onsite': 2,
                             'home_service': 1
                             },
                 'service_2':{
                             'teletherapy':1,
                             'onsite': 1,
                             'home_service': 1
                             }
                 },
                 ...
     }
     ```

   - **other_services (Object)**
     Description of other services offered with different delivery modes including Teletherapy, Onsite, and Home Service. Session type is also indicated.
     ```
      "properties": {
                 ...
                "other_services": {
                  'service_1':{
                             'teletherapy':0,
                             'onsite': 2,
                             'home_service': 1
                             },
                 'service_2':{
                             'teletherapy':1,
                             'onsite': 1,
                             'home_service': 1
                             }
                 },
                 ...
     }
     ```

   - **images (Array)**
     Names of image files associated with the feature (possibly showcasing the therapy center or its services).

   ```
      "properties": {
                 ...
                "images": [
                  {
                             'img_name':'imgname1.jpg',
                             'img_url': 'https://container/imgname1.jpg',
                             },
                 {
                             'img_name':'imgname2.jpg',
                             'img_url': 'https://container/imgname2.jpg',
                             }
                 ],
                 ...
     }
     ```

