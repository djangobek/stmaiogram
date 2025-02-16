import requests
from environs import Env
env = Env()
env.read_env()
import json
URL= f"{env.str('BASE_URL')}/api"
def create_user(telegram_id:str,language:str=None,name:str=None):
    try:
        response = requests.post(url=f"{URL}/botuser/",
                                 data={'telegram_id': telegram_id, 'name': name, 'language': language})
        return 'Ok'
    except:
        return 'Bad'
def get_all_users():
    try:
        response = requests.get(url=f"{URL}/botuser/",
                                 )
        return json.loads(response.text)

    except:
        return []
def get_user(telegram_id):
    try:
        response = requests.post(url=f"{URL}/user/", data={'telegram_id': telegram_id})
        if response.status_code == 204:
            return 'Not Found'
        else:
            return json.loads(response.text)
    except:
        return {}


def change_user_language(telegram_id,language):
    try:
        response = requests.post(url=f"{URL}/lang/", data={'telegram_id': telegram_id, 'language': language})
        if response.status_code == 204:
            return 'Not Found'
        else:
            return json.loads(response.text)
    except:
        pass
def add_channel(channel_id:str,channel_name:str=None,channel_members_count:str=None):
    try:
        response = requests.post(url=f"{URL}/channels/", data={'channel_id': channel_id, 'channel_name': channel_name,'channel_members_count':channel_members_count})
        if response.status_code == 201:
            return 'ok'
        else:
            return 'bad'
    except:
        pass
def get_all_channels():
    try:
        response = requests.get(url=f"{URL}/channels/",
                                 )
        return json.loads(response.text)

    except:
        return []
def get_channel(channel_id):
    try:
        response = requests.post(url=f"{URL}/channel/",
                                 data={'channel_id':channel_id})
        if response.status_code==206:
            return json.loads(response.text)
        else:
            return {}

    except:
        return {}
def delete_channel(channel_id):
    try:
        response = requests.post(url=f"{URL}/delete_channel/",
                                 data={'channel_id':channel_id})
        if response.status_code==200:
            return 'Ok'
        else:
            return "Bad"
    except:
        return "Bad"




def update_user_details(telegram_id: str, first_name: str = None, last_name: str = None):
    """
    Update user's first_name and last_name by telegram_id via the Django API.
    """
    try:
        response = requests.post(
            url=f"{URL}/update-user-details/",
            data={
                'telegram_id': telegram_id,
                'first_name': first_name,
                'last_name': last_name,
            },
        )
        if response.status_code == 200:
            return "User details updated successfully."
        else:
            return f"Failed to update user: {response.json()}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def create_test(name: str = "Test", code: int = None, answers: str = None, type: str = "Test", count: str = None, telegram_id: int = None):
    try:
        # Ensure that the telegram_id is provided
        if not telegram_id:
            return "Error: telegram_id is required."

        # Prepare the data payload
        data = {
            'name': name,
            'code': code,
            'answers': answers,
            'type': type,
            'count': count,
            'telegram_id': telegram_id  # Include telegram_id for the owner
        }

        # Send the POST request
        response = requests.post(
            url=f"{URL}/tests/",
            json=data,  # Use json instead of data to send the data as JSON
        )

        # Check the response status
        if response.status_code == 201:
            return 'Test created successfully'
        else:
            return f"Error creating test: {response.text}"

    except Exception as e:
        return f"An error occurred: {str(e)}"


def get_test_by_code(code):
    try:
        response = requests.get(f"{URL}/tests/", params={'code': code})
        if response.status_code == 200:
            return response.json()  # Return the test data as JSON
        elif response.status_code == 404:
            return "Test not found"
        else:
            return f"Error: {response.text}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


# def get_test_participations(test_id):
#     """
#     Fetch all participations for a specific test.
#     """
#     url = f"{URL}/test/{test_id}/participations/"
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         return {"error": response.json()}
#
# def create_test_participation(data):
#     url = f"{URL}/test/participations/"
#     try:
#         response = requests.post(url, json=data)
#         response.raise_for_status()  # Raise exception for HTTP errors
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"Error in create_test_participation: {e}, Response: {response.text}")
#         return {"error": f"Failed to create participation: {str(e)}"}
#
#
# def get_test_by_code(code):
#     url = f"{URL}/test/?code={code}"
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # Raise exception for HTTP errors
#         return response.json()  # Parse JSON
#     except requests.exceptions.RequestException as e:
#         print(f"Error in get_test_by_code: {e}, Response: {response.text}")
#         return {"error": f"Failed to fetch test: {str(e)}"}


def get_test_by_code(code):
    """
    Fetch a test by its code.
    """
    url = f"{URL}/test/{code}/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching test by code: {e}")
        return {"error": str(e)}


def get_tests_by_owner(owner_id: int):
    """
    Fetch all tests for a specific owner.
    Filters tests based on the owner ID.
    """
    url = f"{URL}/get/test/"  # Endpoint to get all tests
    try:
        response = requests.get(url)
        response.raise_for_status()
        tests = response.json()

        # Filter tests based on the owner_id
        owner_tests = [test for test in tests if test['owner']['telegram_id'] == str(owner_id)]

        return owner_tests
    except requests.exceptions.RequestException as e:
        print(f"Error fetching tests for owner {owner_id}: {e}")
        return {"error": str(e)}

# def get_test_participations(test_id):
#     """
#     Fetch all participations for a specific test.
#     """
#     url = f"{URL}/test/{test_id}/participations/"
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching participations: {e}")
#         return {"error": str(e)}

def get_test_participations(test_id):
    try:
        # Make the API request to fetch participations
        response = requests.get(url=f"{URL}/test/{test_id}/participations/")

        if response.status_code == 200:
            return json.loads(response.text)  # Return the participations data
        elif response.status_code == 404:
            # No participations found; return an empty list
            return []
        else:
            # Raise an exception for unexpected status codes
            response.raise_for_status()
    except Exception as e:
        print(f"Error fetching participations: {str(e)}")
        return []


import logging
logger = logging.getLogger(__name__)


def create_test_participation(user_id, test_id, answers, correct_answer, wrong_answer, certificate):
    """
    Create a new test participation using the backend API.
    """
    try:
        data = {
            'user_id': user_id,
            'test_id': test_id,
            'answers': answers,
            'correct_answer': correct_answer,
            'wrong_answer': wrong_answer,
            'certificate': certificate,
        }
        response = requests.post(url=f"{URL}/test/participationers/post/", json=data)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()  # Return the response as JSON
    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating test participation: {str(e)}")
        return None


def update_test_status_api(test_id):
    """
    Call the API to update the test status.
    """
    try:
        # Make sure the status is either True or False

        # Build the API URL with the status and test_id
        api_url = f"{URL}/update-test-status/{test_id}/"

        # Send a POST request to update the test status
        response = requests.post(api_url)

        # Handle the response
        if response.status_code == 200:
            return response.json()  # Return the success response
        else:
            return {"success": False, "error": response.text}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_files():
    """
    Call the API to get file IDs from the backend.
    """
    try:
        response = requests.get(f'{URL}/files/')

        if response.status_code == 200:
            data = response.json()
            return data.get("file_ids", [])  # FIXED LINE
        else:
            return []
    except Exception as e:
        print(f"Error fetching file IDs: {e}")
        return []