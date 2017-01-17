<a href="https://www.twilio.com">
  <img src="https://static0.twilio.com/marketing/bundles/marketing/img/logos/wordmark-red.svg" alt="Twilio" width="250" />
</a>

# Block Spam Calls. Powered by Twilio - Python/Flask
[![Build
Status](https://travis-ci.org/TwilioDevEd/block-spam-calls-python.svg?branch=master)](https://travis-ci.org/TwilioDevEd/block-spam-calls-python)

Learn how to use Twilio add-ons to block spam calls.

## Local development

First you need to have [python](https://www.python-lang.org/), [virtualenv](https://virtualenv.pypa.io) and [pip](https://pip.pypa.io/) installed on your system.

To run the app locally, clone this repository and `cd` into its directory:

1. First clone this repository and `cd` into its directory:
   ```
   git clone git@github.com:TwilioDevEd/block-spam-calls-python.git

   cd block-spam-calls-python
   ```

1. Create a virtualenv and load it

    ```
    virtualenv venv
    source ./venv/bin/activate
    ```

1. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

1. Run the application.

  ```
  $ python block_spam_calls/app.py
  ```

To actually forward incoming calls, your development server will need to be publicly accessible. [We recommend using ngrok to solve this problem](https://www.twilio.com/blog/2015/09/6-awesome-reasons-to-use-ngrok-when-testing-webhooks.html).

Once you have started ngrok, update your TwiML app's voice URL setting to use your ngrok hostname, so it will look something like this:

```
http://88b37ada.ngrok.io/
```

1. Check it out at [http://localhost:5000](http://localhost:5000)

That's it

## Run the tests

You can run the tests locally by typing

```
python test.py
```

## Meta

* No warranty expressed or implied. Software is as is. Diggity.
* [MIT License](http://www.opensource.org/licenses/mit-license.html)
* Lovingly crafted by Twilio Developer Education.