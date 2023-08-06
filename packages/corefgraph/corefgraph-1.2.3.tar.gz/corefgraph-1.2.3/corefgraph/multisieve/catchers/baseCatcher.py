# coding=utf-8
"""Import(this module) and inherit(BaseCatcher) to create a new catcher.
The system will call the constructor(once) and the catch_mention function for
each plausible mention obtained in the system. The filter calling order is not 
reliable for ALL option.
"""

from logging import getLogger

__author__ = "Josu Bermudez <josu.bermudez@deusto.es>"


class BaseCatcher:
    """ Base class for catchers. To create a new catcher import and inherit from
     this class.
    """

    short_name = "base"
    soft_ne = False

    def __init__(self, graph_builder, extractor):
        self.logger = getLogger("{0}.{1}".format(__name__, self.short_name))
        self.graph_builder = graph_builder
        self.extractor = extractor

    def catch_mention(self, mention_candidate):
        """ Overload this in each catcher.

        :param mention_candidate: The mention to test
        :return: True or False.
        """
        self.logger.warning("catch_mention not override!")
        return False

    def _inside_ne(self, mention_span):
        """ Check if a span is inside any Named entity Mention span  and is not
        the mention.

        :param mention_span: The span of the mention.
        """
        if self.soft_ne:
            return False
        for entity_span in self.extractor.named_entities_span:
            if self.graph_builder.is_inside(mention_span, entity_span):
                return True
        return False
