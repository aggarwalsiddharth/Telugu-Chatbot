Q4.

I have used the file examples.csv in the folder cldf to show top 3 example sentences that show the usage and translation of a language

To implement this, I have created an intent: show_examples and a custom action: action_show_examples

To allow the user to first query the language and then simply ask for examples of the above language, I have used slots to store the language entity which can be used by the action action_show_examples

Usage:

Case - 1:

User: Can you tell me about English?

Rasa: English is ....

Rasa: Did it help you?

User: Yes it did!

User: Can you show some examples

Rasa:
Example1: ...
Example2: ...
Example3: ...



Case - 2:

User: Show example sentences of Hindi

Rasa:
Example1: ...
Example2: ...
Example3: ...
