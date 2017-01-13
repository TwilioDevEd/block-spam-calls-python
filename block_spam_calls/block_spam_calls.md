# Block spam calls with Python

Spam, scams, and robocalls are at best annoying. For high-volume customer service centers, they can significantly impact the bottom line. Let’s leverage the Twilio Marketplace and our Python skills to block spam callers, robocallers, and scammers.

*Before getting started, you should already know how to [handle incoming calls](https://www.twilio.com/docs/guides/voice/how-to-respond-to-incoming-phone-calls-in-csharp) with Twilio.*

## Get a Spam Filtering Add-on

The [Twilio Add-ons Marketplace](https://www.twilio.com/marketplace/add-ons) is a great place to find Add-ons for your Twilio apps. You can integrate third-party technologies without leaving the comfort of the Twilio API. You can access the Add-ons [from your Twilio Console](https://www.twilio.com/console/add-ons). Today, we’re going to look at a few Voice Add-ons that can help us with this spam problem. They are, in no particular order, [Whitepages Pro Phone Reputation](https://www.twilio.com/console/add-ons/XB56520d8bffd66533ca92b398596b8438), [Marchex Clean Call](https://www.twilio.com/console/add-ons/XBac2c99d9c684a765ced0b18cf0e5e1c7), and [Nomorobo Spam Score](https://www.twilio.com/console/add-ons/XBac2c99d9c684a765ced0b18cf0e5e1c7):

[![Voice Spam Add-ons](https://s3.amazonaws.com/com.twilio.prod.twilio-docs/images/Voice_Spam_Add-ons.width-800.png)]

We’ll be writing code to work with all three of these Add-ons, but you can research which one you think will work best for your requirements. Also, keep an eye on the Marketplace, as new Add-ons are always showing up.

## Installing the Add-on

Once you’ve decided on the Add-on you’d like to use, click the [![Install](https://s3.amazonaws.com/com.twilio.prod.twilio-docs/images/Install_Add-on_button.original.png)] button and agree to the terms. In our use case today, we want to make use of these Add-ons while handling incoming voice calls, so make sure the “Incoming Voice Call” box for “Use In” is checked and click “Save” to save any changes:

[![Use in incoming voice call](https://s3.amazonaws.com/com.twilio.prod.twilio-docs/images/Use_in_incoming_voice_call.width-800.png)]

Note the “Unique Name” setting. You need to use this in the code that you will write to read the Add-on’s results. In the code for this guide, we are sticking with the default names.

## Check Phone Number Score in Python

When Twilio receives a phone call for your phone number, it will [send details of the call to your webhook]("../../../../api/twiml/twilio_request") (more on how to configure that later). In your webhook code, you [create a TwiML response]("../../../../api/twiml/your_response") to tell Twilio how to handle the call.

For spam-checking, our code needs to check the spam score of the number and deal with the call differently depending on whether the Add-on considers the caller to be a spammer or not. In our example code here, we’ll return a [<Reject> TwiML tag]("../../../../api/twiml/reject") to send spammers packing and a [<Say> TwiML tag]("../../../../api/twiml/say") to welcome legit callers.

The code is a simple [Flask](http://flask.pocoo.org/) application:

**Block Spam Calls with Python**
```python
from flask import Flask, request
import twilio.twiml
import json

app = Flask(__name__)


@app.route("/", methods=['POST'])
def block_spam_calls():
    resp = twilio.twiml.Response()
    block_call = False

    blocker_addons = {
        "nomorobo_spamscore": should_be_blocked_by_nomorobo,
        "whitepages_pro_phone_rep": should_be_blocked_by_whitepages,
        "marchex_cleancall": should_be_blocked_by_marchex
    }

    if 'AddOns' in request.form:
        add_ons = json.loads(request.form['AddOns'])
        if add_ons['status'] == 'successful':
            for blocker_name, blocker_func in blocker_addons.items():
                should_be_blocked = blocker_func(add_ons['results'].get(blocker_name, {}))
                # print(f'{blocker_name} should be blocked ? {should_be_blocked}')
                block_call = block_call or should_be_blocked

    if block_call:
        resp.reject()
    else:
        resp.say("Welcome to the jungle.")
        resp.hangup()
    return str(resp)


def should_be_blocked_by_nomorobo(nomorobo_spamscore):
    if nomorobo_spamscore.get('status') != 'successful':
        return False
    else:
        score = nomorobo_spamscore['result'].get('score', 0)
        return score == 1


def should_be_blocked_by_whitepages(whitepages):
    if whitepages.get('status') != 'successful':
        return False

    results = whitepages.get('result', {}).get('results', [])
    for result in results:
        if result.get('reputation', {}).get('level', 0) == 4:
            return True

    return False


def should_be_blocked_by_marchex(marchex):
    if marchex.get('status') != 'successful':
        return False

    recommendation = marchex.get('result', {}).get('result', {}).get('recommendation')
    return recommendation == 'BLOCK'


if __name__ == "__main__":
    app.run(debug=True)
```

Notice the code has checks for all three of the Add-ons we mentioned before. The code is written to be very flexible and handle missing data in the JSON response, so feel free to copy and paste even if you only plan to use one of the Add-ons.

### How to Check Whitepages Pro Phone Reputation

Here’s an example of what Whitepages Pro Phone Reputation will return in the “AddOns” form parameter:

**White Pages Pro Reputation Add-on JSON Response**

```json
{
  "status": "successful",
  "message": null,
  "code": null,
  "results": {
    "whitepages_pro_phone_rep": {
      "request_sid": "XRxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      "status": "successful",
      "message": null,
      "code": null,
      "result": {
        "results": [
          {
            "phone_number": "2095551212",
            "reputation": {
              "level": 1,
              "details": [
                {
                  "score": 2,
                  "type": "NotApplicable",
                  "category": "NotApplicable"
                }
              ],
              "volume_score": 1,
              "report_count": 0
            }
          }
        ],
        "messages": [ ]
      }
    }
  }
}
```

The root properties are sent by Twilio. The White Pages Pro Reputation Add-on fill in the dictionary under `whitepages_pro_phone_rep`. We can analyze those information and take a decision as follows:

**Whitepages Pro Phone Reputation Python**

```python
def should_be_blocked_by_whitepages(whitepages):
    if whitepages.get('status') != 'successful':
        return False

    results = whitepages.get('result', {}).get('results', [])
    for result in results:
        if result.get('reputation', {}).get('level', 0) == 4:
            return True

    return False
```

### How to Check Marchex Clean Call

Here’s an example of what Marchex Clean Call will return:

**Marchex Clean Call Add-on JSON result**

```json
{
  "status": "successful",
  "message": null,
  "code": null,
  "results": {
    "marchex_cleancall": {
      "request_sid": "XRxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      "status": "successful",
      "message": null,
      "code": null,
      "result": {
        "result": {
          "recommendation": "PASS",
          "reason": "CleanCall"
        }
      }
    }
  }
}
```

Working with that data in Python can be handled with:

**Marchex Clean Call Python**

```python
def should_be_blocked_by_marchex(marchex):
    if marchex.get('status') != 'successful':
        return False

    recommendation = marchex.get('result', {}).get('result', {}).get('recommendation')
    return recommendation == 'BLOCK'
```

### How to Check Nomorobo Spam Score

Here’s an example of what Nomorobo Spam Score will return:

**Nomorobo Add-on JSON result**

```json
{
  "status": "successful",
  "message": null,
  "code": null,
  "results": {
    "nomorobo_spamscore": {
      "request_sid": "XRxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      "status": "successful",
      "message": null,
      "code": null,
      "result": {
        "status": "success",
        "message": "success",
        "score": 0
      }
    }
  }
}
```

Finally, handling that data in Python:

**Nomorobo Python**

```python
def should_be_blocked_by_nomorobo(nomorobo_spamscore):
    if nomorobo_spamscore.get('status') != 'successful':
        return False
    else:
        score = nomorobo_spamscore['result'].get('score', 0)
        return score == 1
```

### Other Rejection Options

Using <Reject> is the simplest way to turn away spammers. However, you may want to handle them differently. The whole [universe of TwiML](https://www.twilio.com/api/twiml) is open to you. For example, you might want to record the call, have the recording [transcribed using another Add-on](https://www.twilio.com/guides/voice/how-to-use-recordings-add-ons-in-python), and log the transcription somewhere for someone to review.

### Other Call Accept Options

For this example, we’re just greeting the caller. In a real-world scenario, you would likely want to connect the call using [<Dial>]("../../../../api/twiml/dial") (to call another number or [Twilio Client]("../../../../api/client")), [<Enqueue>]("../../../../api/twiml/enqueue") the call to be handled by [TaskRouter]("../../../../api/taskrouter"), or [build an IVR]("https://www.twilio.com/docs/tutorials/walkthrough/ivr-phone-tree/python/flask") using [<Gather>]("../../../../api/twiml/gather").

## Configure Phone Number Webhook

Now we need to configure our Twilio phone number to call our application whenever a call comes in. We just need a public host for our Flask application. You can use [ngrok to test locally](https://www.twilio.com/guides/how-use-ngrok-windows-and-visual-studio-test-webhooks).

Armed with the URL to the application, open the [Twilio Console](https://www.twilio.com/console) and [find the phone number](https://www.twilio.com/console/phone-numbers/incoming) you want to use (or [buy a new number](https://www.twilio.com/console/phone-numbers/search)). On the configuration page for the number, scroll down to "Voice" and next to "A CALL COMES IN," select "Webhook" and paste in the function URL. (Be sure "HTTP POST" is selected, as well.)

## Testing a Blocked Call

You can quickly call your Twilio number to make sure your call goes through. However, how can we test a blocked spam result? The easiest way is to write some unit tests that pass some dummied up JSON to our controller action. For example, if we wanted to test a Nomorobo “BLOCK” recommendation, we could use the following JSON:

With that as our test fixture, we can write a test like the following to ensure that our call is blocked when we see the right data in the AddOns JSON:

For a full solution with all the tests for each of the Add-on providers, see our [GitHub repository](https://github.com/TwilioDevEd/twilio-samples-csharp/blob/master/BlockSpamCalls.Test/VoiceControllerTest.cs).

## What’s Next?

As you can see, the Twilio Add-ons Marketplace gives you a lot of options for extending your Twilio apps. Next, you might want to dig into the [Add-ons reference](https://www.twilio.com/api/add-ons) or perhaps glean some pearls from our other [Python tutorials](https://www.twilio.com/tutorials?filter-language=python). Wherever you’re headed next, you can confidently put spammers in your rearview mirror.
