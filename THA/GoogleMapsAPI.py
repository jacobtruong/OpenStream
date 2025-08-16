import googlemaps
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GoogleMapsAPI():
    """
    A class to create and manage interactions with the Google Maps API.
    """

    def __init__(self):
        """
        Initialise a Google Maps API client.
        """
        self.map_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        
        if not self.map_api_key:
            raise ValueError("Google Maps API key is required.")
        
        self.maps_client = googlemaps.Client(key=self.map_api_key)

    def extract_location_info_from_address(self, address: str) -> dict:
            """
            Extracts location information from a given address.

            Args:
                address (str): The address to extract location information from.

            Returns:
                dict: A dictionary containing location information (city, state, country) or an empty dictionary if not found.
            """

            try:
                # Geocode the address
                geocode_result = self.maps_client.geocode(address)

                if not geocode_result:
                    return {}
                
                components = geocode_result[0]['address_components']
                
                city = state = country = None
                
                for component in components:
                    types = component['types']
                    if 'locality' in types:
                        city = component['long_name']
                    elif 'administrative_area_level_1' in types:
                        state = component['long_name']
                    elif 'country' in types:
                        country = component['long_name']
                
                return {'city': city, 'state': state, 'country': country}
            except Exception as e:
                logging.error(f"Failed to extract location information: {e}")
                return {}

    def get_satellite_image_bytes(self, address: str, zoom_factor: float) -> bytes:
        """
        Retrieves a satellite image for a given address using the Google Maps Static API.

        Args:
            address (str): The address to retrieve the satellite image for.
            zoom_factor (float): The zoom level for the satellite image.

        Returns:
            bytes: The satellite image bytes or an empty bytes object if retrieval failed.
        """
        try:
            image_data_generator = self.maps_client.static_map(
                center=address,
                zoom=zoom_factor,
                size=(800, 600),
                maptype='satellite'
            )

            image_data = b''.join(image_data_generator)
            return image_data if image_data else b''
        except Exception as e:
            logging.error(f"Failed to retrieve satellite image: {e}")
            return b''