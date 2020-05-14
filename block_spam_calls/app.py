#!/usr/bin/env python3
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
import json

app = Flask(__name__)


@app.route("/", methods=['POST'])
def block_spam_calls():
    resp = VoiceResponse()
    block_call = False

    blocker_addons = {
        "nomorobo_spamscore": should_be_blocked_by_nomorobo,
        "ekata_phone_valid": should_be_blocked_by_ekata,
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


def should_be_blocked_by_ekata(ekata):
    if ekata.get('status') != 'successful':
        return False
    return ekata['result']['reputation_level'] >= 4


def should_be_blocked_by_marchex(marchex):
    if marchex.get('status') != 'successful':
        return False

    recommendation = marchex.get('result', {}).get('result', {}).get('recommendation')
    return recommendation == 'BLOCK'


if __name__ == "__main__":
    app.run(debug=True)
