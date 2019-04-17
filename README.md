# Recurrent Neural Net LSTM Keystroke Dynamics Model

This repository seeks to recreate the model described in the paper "Recurrent neural network-based user authentication for freely typed keystroke data". 

Towards this purpose, I collected data, not included for privacy concerns,  using a custom Rails application which contained the keystroke times unique to each individual at 10,000 keystrokes each. Because this approach focuses on training based on the individual, instead of comparatively classifying to imposters, it was determined that a large number of individuals was unnecessary for testing anything other than the equal error rate of the models.

You can find the details of the model in the references/rnn_based_user_auth_for_free_typing.pdf though they can be simplified as follows:
* Collect keystroke data
* Transform data into concatenated one hot encodings 
* Train the model based on training/validation data
* Use the network loss function to calculate a novelty score
* Calculate the FAR/FRR from imposter versus user data, find the novelty score and percentage at which they meet.
* Use the threshold to "authenticate" users with a certainty of said EER