<a href="https://www.twilio.com">
  <img src="https://static0.twilio.com/marketing/bundles/marketing/img/logos/wordmark-red.svg" alt="Twilio" width="250" />
</a>

# Block Spam Calls. Powered by Twilio - Python/Flask

![](https://github.com/TwilioDevEd/block-spam-calls-python/workflows/Flask/badge.svg)

> We are currently in the process of updating this sample template. If you are encountering any issues with the sample, please open an issue at [github.com/twilio-labs/code-exchange/issues](https://github.com/twilio-labs/code-exchange/issues) and we'll try to help you.

Learn how to use Twilio add-ons to block spam calls. Learn more about what's needed from this 
[Twilio guide](https://www.twilio.com/docs/guides/block-spam-calls-and-robocalls-python).

## Local development

First you need to have [python](https://www.python.org/), [virtualenv](https://virtualenv.pypa.io) and [pip](https://pip.pypa.io/) installed on your system.

To run the app locally, clone this repository and `cd` into its directory:

1. First clone this repository and `cd` into its directory:
   ```
   git clone https://github.com/TwilioDevEd/block-spam-calls-python.git
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
    python block_spam_calls/app.py
    ```

To actually forward incoming calls, your development server will need to be publicly accessible. [We recommend using ngrok to solve this problem](https://www.twilio.com/blog/2015/09/6-awesome-reasons-to-use-ngrok-when-testing-webhooks.html).

Once you have started ngrok, update your TwiML app's voice URL setting to use your ngrok hostname, so it will look something like this:

```
http://88b37ada.ngrok.io/
```

## Run the tests

You can run the tests locally by typing

```
python test.py
```

## Meta

* No warranty expressed or implied. Software is as is. Diggity.
* The CodeExchange repository can be found [here](https://github.com/twilio-labs/code-exchange/).
* [MIT License](http://www.opensource.org/licenses/mit-license.html)
* Lovingly crafted by Twilio Developer Education.
