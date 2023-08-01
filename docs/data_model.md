# Data Model Description

This data model describes a single feature in Ausome Maps, representing a therapy center for differently-abled individuals. The feature has both geometric and property information. Below is the breakdown of each part of the data model:

1. **geometry**

   - **type (Point)**
   
      The type of the feature, which is "Point" in this case, indicating that the data represents a geographic point location.

   - **coordinates (LatLng)**
  
     Contains the geographical coordinates (longitude, latitude, and altitude) of the therapy center, represented as a "Point" type.

2. **properties**

   This section includes various properties of the therapy center:

   - **date_updated (DateTime)**

     The end date and time of the feature entry (in the format "YYYY-MM-DDTHH:mm:ss.sss+08:00").

   - **info_src_name (String)**

     Name of the information source. ("Garry Louie Sabado" in this case)

   - **info_src_designation (String)**

     Designation/role of the information source ("Managing Director").

   - **placename (String)**
     Name of the therapy center ("K-Time Early Intervention Therapy Center").

   - **address (String)**
     Physical address of the therapy center ("20 Pangustura St., Midtown Subd. Ph-3, San Roque, Marikina City, Metro Manila, 1801").

   - **region (String)**
     Region where the therapy center is located ("NCR – National Capital Region").

   - **city (String)**
     City where the therapy center is situated ("Marikina City").

   - **landmarks_desc (String)**
     Description of nearby landmarks ("Right beside 20 Studio Hotel").

   - **contact_number (String)**
     Primary contact number of the therapy center ("09175136863").

   - **alt_contact_number (String)**
     Alternative contact number ("02-8635-6808").

   - **email_address (String)**
     Email address of the therapy center ("ktimeeic@gmail.com").

   - **website (String)**
     Website URL of the therapy center ("https://ktimeeic.wixsite.com/kteic").

   - **facebook (String)**
     Indicates if the therapy center has a presence on Facebook ("K-Time Early Intervention Therapy Center").

   - **instagram (String)**
     Indicates if the therapy center has a presence on Instagram ("ktimeph").

   - **caters_to (String)**
     Describes the target populations the therapy center caters to ("Pediatric Population Adolescent Population Adult Population").

   - **Various services offered**
     The following attributes indicate the types of services offered by the therapy center, specifying whether they are provided to individuals, groups, or through teletherapy, as well as home service options.

   - **other_services (String)**
     Description of other services offered, including "Behavioral Therapy" with different delivery options (Teletherapy, On-Site, Home Service).

   - **img_1, img_2, img_3 (String)**
     Names of image files associated with the feature (possibly showcasing the therapy center or its services).

   - **img_1_url, img_2_url, img_3_url (String)**
     URLs to access the respective images online.

This data model description provides a comprehensive overview of the feature entry for the K-Time Early Intervention Therapy Center on Ausome Maps, capturing essential details about the center's location, services, contact information, and related media. It also highlights the different types of therapy options available and the target populations catered to by the therapy center.
