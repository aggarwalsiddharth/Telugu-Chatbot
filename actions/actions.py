# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

#
#
from googletrans import Translator
translator = Translator(service_urls=['translate.googleapis.com'])
#
#
import pandas as pd
import os
import time

class ActionLanguageSearch(Action):

    def name(self) -> Text:
        return "action_lang_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        data_path = os.path.join("data", "cldf-datasets-wals-014143f", "cldf", "languages.csv")
        wals_data = pd.read_csv(data_path)
        entities = list(tracker.get_latest_entity_values("language"))

        if len(entities) > 0:
            #print("entit>0")
            query_lang = entities.pop()
            #print(f'query lang is {query_lang}')

            query_lang_en = translator.translate(query_lang, dest='en').text
            query_lang_en = query_lang_en.lower().capitalize()
            if query_lang == 'తెలుగు':
            #    print('Hi')
                query_lang_en = 'Telugu'
            #print(f'in english {query_lang_en}')

            
            out_row = wals_data[wals_data["Name"] == query_lang_en].to_dict("records")

            if len(out_row) > 0:
                out_row = out_row[0]
                _name = translator.translate(out_row["Name"], dest='te').text
                _family = translator.translate(out_row["Family"], dest='te').text
                _genus = translator.translate(out_row["Genus"], dest='te').text
                out_text = "భాష %s కుటుంబానికి చెందినది %s జాతితో %s మరియు ISO కోడ్ %s" % (_name, _family, _genus, out_row["ISO_codes"])
                
                language_name = tracker.get_slot("language")

                dispatcher.utter_message(text = out_text)
                dispatcher.utter_message(text = 'అది మీకు సహాయం చేసిందా?')
            else:
                language_name = None
                dispatcher.utter_message(text = "క్షమించండి! భాష %s కోసం మాకు రికార్డులు లేవు" % query_lang)
        else:
            language_name = None
            dispatcher.utter_message(text = "క్షమించండి! అది నాకు అర్థం కాలేదు")

        return [SlotSet("language",language_name)]

class ActionShowExamples(Action):

    def name(self) -> Text:
        return "action_show_examples"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        data_path = os.path.join("data", "cldf-datasets-wals-014143f", "cldf", "languages.csv")
        wals_data = pd.read_csv(data_path)
        ex_path = os.path.join("data", "cldf-datasets-wals-014143f", "cldf", "examples.csv")
        ex_data = pd.read_csv(ex_path)
        entity = tracker.get_slot("language")
        #print(entity)


        if entity:
            query_lang = entity
            query_lang_en = translator.translate(query_lang, dest='en').text

            query_lang_en = query_lang_en.lower().capitalize()
            #print(query_lang_en)
            
            out_row = wals_data[wals_data["Name"] == query_lang_en].to_dict("records")

            if len(out_row) > 0:
                out_row = out_row[0]
                lang_id = out_row['ID']

                ex_list = ex_data[ex_data["Language_ID"]==lang_id]

                if len(ex_list)>0:
                    max_ind = min(3,len(ex_list))
                    for ind,row in ex_list.reset_index(drop=True)[:max_ind].iterrows():
                        out_text = "ఉదాహరణ %s: %s \n " %(translator.translate(ind+1, dest='te').text,row['Primary_Text'])
                        dispatcher.utter_message(text = out_text)
                #out_text = "Language %s belongs to the Family %s\n with Genus as %s\n and has ISO code %s" % (out_row["Name"], out_row["Family"], out_row["Genus"], out_row["ISO_codes"])
                
                #language_name = tracker.get_slot("language")
                else:
                    dispatcher.utter_message(text = "క్షమించండి! భాష %s కు మాకు ఉదాహరణలు లేవు" % query_lang)
            else:
                dispatcher.utter_message(text = "క్షమించండి! %s భాషకు మా వద్ద రికార్డులు లేవు" % query_lang)

               
        return []
        