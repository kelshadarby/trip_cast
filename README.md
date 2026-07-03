# TripCast (Work in Progress)

A Django REST Framework backend API for a road trip weather planning application. TripCast allows users to plan road trips by calculating routes, searching for stops along the way, and viewing weather forecasts at each stop. Designed to connect to a React Native mobile frontend (to be created) with a toggleable radar map overlay powered by AccuWeather.

---

## Setup

### Dependencies

- [Django REST Framework](https://www.django-rest-framework.org/)
  * Provides API views, serializers, and JSON response handling for all TripCast endpoints.

- [django-cors-headers](https://pypi.org/project/django-cors-headers/)
  * Allows the Django backend to accept requests from the React Native frontend running on a different origin.

- [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/)
  * Handles JWT token-based authentication for user accounts and protected routes.

- [requests](https://pypi.org/project/requests/)
  * Used to make outbound HTTP requests to Google and AccuWeather APIs from Django services.

### External APIs Required

You will need API keys for the following services:

- [Google Routes API](https://developers.google.com/maps/documentation/routes) — route calculation
- [Google Places API](https://developers.google.com/maps/documentation/places/web-service) — search along route
- [Google Geocoding API](https://developers.google.com/maps/documentation/geocoding) — coordinate lookup
- [Google Weather API](https://developers.google.com/maps/documentation/weather) — weather forecasts
- [AccuWeather Radar API](https://developer.accuweather.com/) — radar map tiles

### Installation

**Mac OS X / Linux:**
```bash
git clone https://github.com/kelshadarby/trip_cast
cd trip_cast
python -m venv venv
source venv/bin/activate
pip install django djangorestframework djangorestframework-simplejwt requests django-cors-headers
```

**Windows:**
```bash
git clone https://github.com/kelshadarby/trip_cast
cd trip_cast
python -m venv venv
venv\Scripts\activate
pip install django djangorestframework djangorestframework-simplejwt requests django-cors-headers
```

### Getting Started

1. Add your API keys to `trip_cast/settings.py`:
```python
GOOGLE_API_KEY = 'your_google_api_key_here'
ACCUWEATHER_API_KEY = 'your_accuweather_api_key_here'
```

2. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Start the development server:
```bash
python manage.py runserver
```

---

## Usage

### Apps and Endpoints

**Waypoint** — `/api/waypoint/`

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/waypoints/search/` | Search for places using Google Places API |
| POST | `/api/waypoints/create/` | Save a waypoint to the database |

**Route** — `/api/route/`

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/route/create/` | Calculate and save a route between two waypoints |
| GET | `/api/route/<route_id>/` | Retrieve a saved route |
| PATCH | `/api/route/update/endpoints/<route_id>/` | Update origin or destination |
| DELETE | `/api/route/delete/<route_id>/` | Delete a route |

**Route Waypoint (In Progress)** — `/api/route/<route_id>/waypoint/`

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/route/<route_id>/search/` | Search for places along a route polyline |
| POST | `/api/routes/<route_id>/waypoint/<waypoint_id>/add/` | Save a rest stop to a trip |

### Example Request — Create a Route

```bash
POST /api/route/create/
Content-Type: application/json

{
    "origin_waypoint_id": 1,
    "destination_waypoint_id": 2
}
```

**Response:**
```json
{
    "id": 1,
    "origin": 1,
    "destination": 2,
    "polyline": "encoded_polyline_string",
    "total_distance_meters": 680450,
    "total_duration_seconds": "25234s"
}
```

---

## Project Structure
trip_cast/          ← project config
waypoint/           ← waypoint search and storage
route/              ← route calculation and management, also holds waypoints along a route (in progress)

---

## Work In Progress

The following features are planned but not yet implemented:

- Adding stops to a route (currently in progress)
- User authentication (JWT)
- Weather forecasts at each stop
- AccuWeather radar tile integration
- Trip saving to user profiles
- React Native frontend

---

## Team

* Kelsha — Solo developer, backend architecture and API integration

---

## Errors and Bugs

If something is not behaving intuitively, it is a bug and should be reported.
Report it here by creating an issue on GitHub.

Follow [Mozilla's guidelines for reporting bugs](https://developer.mozilla.org/en-US/docs/Mozilla/QA/Bug_writing_guidelines#General_Outline_of_a_Bug_Report) to help fix issues quickly.

---

## Patches and Pull Requests

* Fork the project
* Make your feature addition or bug fix
* Send a pull request with a description of your work

---

## Copyright and Attribution

Copyright (c) 2026 Kelsha. Released under the [MIT License](https://github.com/your-repo-here/blob/master/LICENSE)
