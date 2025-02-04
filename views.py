from django.shortcuts import render
from django.http import JsonResponse
from .models import UserProfile
import requests
from django.shortcuts import redirect
# SnapSynth API URL
SNAP_SYNTH_API_URL = "http://127.0.0.1:8001/generate_html_and_css"

def generate_ui(request, username):
    """ View to handle dynamic UI generation using SnapSynth """
    
    try:
        user = UserProfile.objects.get(username=username)
        context = {"username": user.username, "email": user.email, "account_balance": user.account_balance, "recent_transactions": user.transactions.all()[:5]}

        # Only trigger SnapSynth API on form submission (POST request)
        if request.method == "POST":
            payload = {
                "username": user.username,
                "account_balance": user.account_balance,
                "recent_transactions": [
                    {"date": tx.date.strftime("%Y-%m-%d"), "description": tx.description, "amount": tx.amount}
                    for tx in user.transactions.all()
                ],

            }

            # Send a POST request to SnapSynth API
            response = requests.post(SNAP_SYNTH_API_URL, json=payload)

            if response.status_code == 200:
                response_data = response.json()
                html = response_data.get("html", "")
                css = response_data.get("css", "")
                context.update({"generated_html": html, "generated_css": css})
            else:
                return JsonResponse({"error": "Failed to update the UI with SnapSynth"}, status=400)

        # Return the user profile page with or without generated UI
        return render(request, "user_profile/user_profile.html", context)

    except UserProfile.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
def profile(request, username):
    """ View to display the user profile page """
    try:
        # Query the UserProfile model based on the username
        user_profile = UserProfile.objects.get(user__username=username)

        # Prepare context data with user profile info
        context = {
            "username": user_profile.user.username,  # Get the username from the User model
            "email": user_profile.user.email,  # Get the email from the User model
            "account_balance": user_profile.balance,
            "recent_transactions": user_profile.transactions[:5],  # Assuming it's a list of transactions
            "location": user_profile.location,
            "current_location": user_profile.current_location,
        }

        # Render the user profile page with the user data
        return render(request, "user_profile/user_profile.html", context)

    except UserProfile.DoesNotExist:
        # Handle user profile not found
        return render(request, "user_profile/error.html", {"error": "User profile not found."})
    except Exception as e:
        # Handle any other errors
        return render(request, "user_profile/error.html", {"error": str(e)})

def login_success(request):
    """Redirect authenticated users to their profile page."""
    if request.user.is_authenticated:
        return redirect(f'/user/profile/{request.user.username}/')  # Ensure correct URL
    return redirect('login')

