__author__ = 'saba.teserra'



def get_bigram_context(bigrams, search_terms, monograms):
   bigram_context = {}
   for bg in bigrams.keys():

      for term in search_terms:


        if bg in term and len(bg) < len(term):
            bg_last_term = bg.split()[1]
            words =term.split()
            i = 0
            while i < len(words):
                if words[i] == bg_last_term and i+1 < len(words):
                  if words[i+1] in monograms.keys():
                    if bg not in bigram_context.keys():
                       bigram_context[bg] ={words[i+1]:monograms[words[i+1]]}
                    else:
                        context = bigram_context[bg]
                        if words[i+1] in context.keys():
                            context[words[i+1]] += 1
                            bigram_context[bg] = context
                        else:
                            context[words[i+1]] = monograms[words[i+1]]
                            bigram_context[bg] = context

                i += 1
   return bigram_context

def get_monogram_context(search_terms, monograms):
   monogram_context = {}
   for mg in monograms.keys():
      for term in search_terms:
        if mg in term and len(mg) < len(term):
            words =term.split()
            i = 0
            while i < len(words):
                if words[i] == mg and i+1 < len(words):
                   if words[i+1] in monograms.keys():

                    if mg not in monogram_context.keys():
                       monogram_context[mg] ={words[i+1]:monograms[words[i+1]]}
                    else:
                        context = monogram_context[mg]
                        if words[i+1] in context.keys():
                            context[words[i+1]] += 1
                            monogram_context[mg] = context
                        else:
                            context[words[i+1]] = monograms[words[i+1]]
                            monogram_context[mg] = context

                i += 1
   return monogram_context
