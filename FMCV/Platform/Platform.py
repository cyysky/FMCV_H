import FMCV.Platform.Dobot as Dobot
#import Jaka
import functools


class Platform:
    @staticmethod
    def platform_factory(model="", feedback_callback=None):
        """This static factory method will create and return the instance of input model"""
        if (model == "Dobot.MG400"):
            return Dobot.MG400(feedback_callback)
        elif (model == "Jaka.MiniCobot"):
            #TODO: return Jaka.MiniCobot(feedback_callback)
            return None
        else:
            # Cannot resolve the input model name, return nothing
            return None

    @staticmethod
    def isSubstringExists(mainstring="", substrings=[]):
        if (len(substrings) > 0):
            # initiate the 1st element to False, this won't affect the final "OR" result
            available = [False]

            # Get individual results of substrings exists in mainstring or not, and make it into a list
            mapping_list = [(x in mainstring) for x in substrings]
            available.extend(mapping_list)

            # Aggregate the available list by "OR" the whole list into single result
            return functools.reduce(lambda x, y: x or y, available)
        else:
            return False

    @staticmethod
    def available_models(filters=[]):
        """This method will return the list of available models"""
        #models = ["Dobot.MG400", "Jaka.MiniCobot", "Dobot.test", "Dobot.test2", "Jaka.MiniCobot1"]
        models = ["Dobot.MG400", "Jaka.MiniCobot"]
        if(len(filters) > 0):
            available_list = [x for x in models if Platform.isSubstringExists(x, filters)]
        else:
            available_list = models

        return available_list

