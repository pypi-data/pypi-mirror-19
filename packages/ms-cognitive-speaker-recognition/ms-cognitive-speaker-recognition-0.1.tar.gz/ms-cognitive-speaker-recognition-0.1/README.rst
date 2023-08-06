ms-cognitive-speaker-recognition (cognitive_sr)
===============================================

Python 2/3 client for the Microsoft Speaker Recognition API (Microsoft Cognitive Services)

https://www.microsoft.com/cognitive-services/en-us/speaker-recognition-api

See the examples folder for end to end demonstration.


.. code-block:: python

    import cognitive_sr

    speech_identification = cognitive_sr.SpeechIdentification(subscription_key)

    result = speech_identification.identify_profile(profile_ids, wav_data)

    print('Identified wav as profile: ', result['identifiedProfileId'])
    print('Confidence is: ', result['confidence'])


Installation
------------

To install, simply:

.. code-block:: bash

    $ pip install ms-cognitive-speaker-recognition

