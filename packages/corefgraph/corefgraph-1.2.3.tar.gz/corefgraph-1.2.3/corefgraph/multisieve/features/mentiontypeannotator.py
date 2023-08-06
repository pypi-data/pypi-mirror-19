# coding=utf-8
""" Annotation of the mention type and subtype.
"""

from corefgraph.multisieve.features.constants import MENTION, STARTED_BY_INDEFINITE_ARTICLE, \
    STARTED_BY_INDEFINITE_PRONOUN, PRONOUN_MENTION, NOMINAL_MENTION, \
    PROPER_MENTION, RELATIVE_PRONOUN, ENUMERATION_MENTION

from corefgraph.constants import POS, FORM, LABEL, HEAD_OF_NER, SPAN
from corefgraph.multisieve.features.baseannotator import FeatureAnnotator
from corefgraph.resources.dictionaries import pronouns, determiners
from corefgraph.resources.tagset import pos_tags, ner_tags

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'
__date__ = '3/19/14'


class MentionTypeAnnotator(FeatureAnnotator):
    """Annotate the type of a mention(nominal, pronominal, pronoun) also search
    some relevant features of the mention(Mention subtype)"""

    name = "type"
    features = [STARTED_BY_INDEFINITE_ARTICLE, STARTED_BY_INDEFINITE_PRONOUN,
                MENTION, RELATIVE_PRONOUN]
    

    @staticmethod
    def _set_mention_type(node, mention_type):
        """ The node is set as a mention of the specify type.

        :param node: The node to be set as mention.
        :param mention_type: The mention type used to set the node.
        """
        node[MENTION] = mention_type
        node[LABEL] = node[LABEL] + "\n" + mention_type
    
    def extract_and_mark(self, mention):
        """ Determine the type of the mention. Also check some mention related
        features.

        :param mention: The mention to be classified.
        """
        words = self.graph_builder.get_words(mention)
        head = self.graph_builder.get_head_word(mention)
        head_pos = head[POS]
        head_form = head[FORM].lower()
        head_word_ner = head.get(HEAD_OF_NER)
        first_form = words[0][FORM].lower()
        if pronouns.relative(first_form) and len(words) == 1:
            mention[RELATIVE_PRONOUN] = True
        else:
            mention[RELATIVE_PRONOUN] = False
        
        if determiners.indefinite_articles(first_form):
            mention[STARTED_BY_INDEFINITE_ARTICLE] = True
        else:
            mention[STARTED_BY_INDEFINITE_ARTICLE] = False
        
        if pronouns.indefinite(first_form):
            mention[STARTED_BY_INDEFINITE_PRONOUN] = True
        else:
            mention[STARTED_BY_INDEFINITE_PRONOUN] = False
        # Enumeration mention
        if self.is_enumeration(mention):
            self._set_mention_type(mention, ENUMERATION_MENTION)
        # Pronoun mention
        elif (len(words) == 1 and pos_tags.pronouns(head_pos)) or\
                (len(words) == 1 and (pronouns.all_pronouns(head_form) or pronouns.relative(head_form)) and
                 not ner_tags.mention_ner(head_word_ner)):
            self._set_mention_type(mention, PRONOUN_MENTION)
        # Proper Mention
        elif pos_tags.proper_nouns(head_pos) or ner_tags.all(head_word_ner):
            self._set_mention_type(mention, PROPER_MENTION)
        # In other case is nominal
        else:
            self._set_mention_type(mention, NOMINAL_MENTION)

    def is_enumeration(self, mention):
        sentence_words = self.graph_builder.get_words(self.graph_builder.get_root())
        commas = 0
        for word in self.graph_builder.get_words(mention):
        #for word in self.graph_builder.get_syntactic_children(mention):
            if word[FORM] == ",":
                commas += 1
                if commas > 2:

                    return True
            if pos_tags.conjunctions(word.get(POS)):
                return True
        return False

    def is_enumeration(self, mention):
        commas = 0
        mention_words = self.graph_builder.get_words(mention)
        last_comma = 0
        last_conjuction = 0
        # for word in self.graph_builder.get_syntactic_children(mention):
        for index,word in enumerate(mention_words):
            #if word[FORM] == ",":
            #    commas += 1
            #if pos_tags.conjunctions(word.get(POS)):
            #    return True
            if word[FORM] == ",":
                last_comma = index
            if pos_tags.conjunctions(word.get(POS)):
                last_conjuction = index
        if last_conjuction and last_conjuction > last_comma:
            return True
        # if commas:
        #     for word in self.graph_builder.get_words(self.graph_builder.get_root(mention)):
        #         if pos_tags.conjunctions(word.get(POS)) and word[SPAN][0] > mention_words[-1][SPAN][1]:
        #             return True
        #     return True
        return False

