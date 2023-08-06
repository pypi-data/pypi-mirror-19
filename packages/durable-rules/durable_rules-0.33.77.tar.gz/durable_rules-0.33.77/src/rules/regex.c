
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "rules.h"
#include "rete.h"
#include "regex.h"

#define REGEX_SYMBOL 0x00
#define REGEX_UNION 0x01
#define REGEX_STAR 0x02
#define REGEX_PLUS 0x03
#define REGEX_QUESTION 0x04
#define REGEX_INTERVAL 0x05
#define REGEX_REGEX 0x06
#define REGEX_DOT 0xFFFE

#define MAX_TRANSITIONS 0xFFFF
#define MAX_QUEUE 1024
#define MAX_STATES 512
#define MAX_SET 1024
#define MAX_LIST 1024
#define MAX_INTERVAL 100


#define CREATE_QUEUE(type) \
    type queue[MAX_QUEUE]; \
    unsigned short first = 0; \
    unsigned short last = 0; \

#define ENQUEUE(value) do { \
    if ((last + 1) == first) { \
        return ERR_REGEX_QUEUE_FULL; \
    } \
    queue[last] = value; \
    last = (last + 1) % MAX_QUEUE; \
} while(0)

#define DEQUEUE(value) do { \
    if (first == last) { \
        *value = 0; \
    } else { \
        *value = queue[first]; \
        first = (first + 1) % MAX_QUEUE; \
    } \
} while(0)

#define CREATE_LIST(type) \
    type list[MAX_QUEUE]; \
    unsigned short top = 0;

#define LIST_EMPTY() !top

#define ADD(value) do { \
    if ((top + 1) == MAX_LIST) { \
        return ERR_REGEX_LIST_FULL; \
    } \
    list[top++] = value; \
    for (unsigned short i = top - 1; (i > 0) && (list[i]->id < list[i - 1]->id); --i) {\
        state *temp = list[i]; list[i] = list[i - 1]; list[i - 1] = temp; \
    } \
} while(0)

#define LIST list, top

#define CREATE_HASHSET(type) \
    type set[MAX_SET] = {NULL}; \

#define HSET(value) do { \
    unsigned int size = 0; \
    unsigned short index = value->hash % MAX_SET; \
    while (set[index]) { \
        index = (index + 1) % MAX_SET; \
        ++size; \
        if (size == MAX_SET) { \
            return ERR_REGEX_SET_FULL; \
        } \
    } \
    set[index] = value; \
} while(0)

#define HGET(valueHash, value) do { \
    unsigned short index = valueHash % MAX_SET; \
    *value = NULL; \
    while (set[index] && !*value) { \
        if (set[index]->hash == valueHash) { \
            *value = set[index]; \
        } \
        index = (index + 1) % MAX_SET; \
    } \
} while(0)

#define HASHSET set

#define CREATE_STATE(stateId, newState) do { \
    unsigned int result = createState(stateId, newState); \
    if (result != RULES_OK) { \
        return result; \
    } \
} while (0)

#define LINK_STATES(previousState, nextState, tokenSymbol) do { \
    unsigned int result = linkStates(previousState, nextState, tokenSymbol); \
    if (result != RULES_OK) { \
        return result; \
    } \
} while (0)

struct state;

typedef struct transition {
    unsigned short symbol;
    struct state *next;
} transition;

typedef struct state {
    unsigned int hash;
    unsigned short refCount;
    unsigned short id;
    unsigned short transitionsLength;
    unsigned char isAccept;
    unsigned char isReject;
    transition transitions[MAX_TRANSITIONS];
} state;

typedef struct token {
    unsigned char type;
    unsigned short low;
    unsigned short high;
    unsigned short symbolsLength;
    unsigned short symbols[MAX_TRANSITIONS];
    unsigned short inverseSymbolsLength;
    unsigned short inverseSymbols[MAX_TRANSITIONS];
} token;

static const unsigned int UTF8_OFFSETS[6] = {
    0x00000000UL, 0x00003080UL, 0x000E2080UL,
    0x03C82080UL, 0xFA082080UL, 0x82082080UL
};

static const char UTF8_TRAILING[256] = {
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
    2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2, 3,3,3,3,3,3,3,3,4,4,4,4,5,5,5,5
};

static const unsigned short EMPTY = 0;

unsigned int utf8ToUnicode(char **first, char *last, unsigned short *result) {
    unsigned char byteNumber = UTF8_TRAILING[(unsigned char)*first[0]];
    if (*first + byteNumber >= last) {
        return ERR_PARSE_REGEX;
    }
    
    *result = 0;
    switch (byteNumber) {
        case 3: 
            *result += (unsigned char)*first[0]; 
            *result <<= 6;
            ++*first;
        case 2: 
            *result += (unsigned char)*first[0]; 
            *result <<= 6;
            ++*first;
        case 1:
            *result += (unsigned char)*first[0]; 
            *result <<= 6;
            ++*first;
        case 0:
            *result += (unsigned char)*first[0];
            ++*first;
    }
    *result -= UTF8_OFFSETS[byteNumber];
    return REGEX_PARSE_OK;
}

static unsigned int readInternalRange(char *first,
                                      unsigned short *rangeLength,
                                      unsigned short *range);

static unsigned int readEscapedSymbol(char **first, 
                                      char *last,
                                      unsigned short *rangeLength, 
                                      unsigned short *range) {
    ++*first;
    if (*first >= last) {
        return ERR_PARSE_REGEX;
    }

    switch (*first[0]) {
        case '.':
        case '|':
        case '?':
        case '*':
        case '+':
        case '(':
        case ')':
        case '[':
        case ']':
        case '{':
        case '}':
        case '%':
            range[*rangeLength] = *first[0];
            ++*rangeLength;
            ++*first;
            return REGEX_PARSE_OK;
        case 'a':
            ++*first;
            return readInternalRange("[\x41-\x5A\x61-\x7A\xC3\x80-\xC3\x96\xC3\x98-\xC3\xB6\xC3\xB8-\xC3\xBF]", rangeLength, range);
        case 'c':
            ++*first;
            return readInternalRange("[\x00-\x1F\x7F\xC2\x80-\xC2\x9F]", rangeLength, range);
        case 'd':
            ++*first;
            return readInternalRange("[0-9]", rangeLength, range);
        case 'g':
            ++*first;
            return readInternalRange("[\x21-\x7E]", rangeLength, range);
        case 'l':
            ++*first;
            return readInternalRange("[\x61-\x7A\xC3\x9F-\xC3\xB6\xC3\xB8-\xC3\xBF]", rangeLength, range);
        case 'p':
            ++*first;
            return readInternalRange("[.,;:?!'\"()\xC2\xA1\xC2\xBF-]", rangeLength, range);
        case 's':
            ++*first;
            return readInternalRange("[\x09-\x0D\x20]", rangeLength, range);
        case 'u':
            ++*first;
            return readInternalRange("[\x41-\x5A\xC3\x80-\xC3\x96\xC3\x98-\xC3\x9E]", rangeLength, range);
        case 'w':
            ++*first;
            return readInternalRange("[A-Za-z0-9]", rangeLength, range);
        case 'x':
            ++*first;
            return readInternalRange("[0-9A-Fa-f]", rangeLength, range);       
    }

    return ERR_PARSE_REGEX;
}

static unsigned int readRange(char **first,
                              char *last, 
                              unsigned short *rangeLength,
                              unsigned short *range,
                              unsigned short *inverseRangeLength,
                              unsigned short *inverseRange) {
    unsigned char parseBegin = 1;
    unsigned short lastSymbol = 0;
    unsigned short currentSymbol;
    unsigned char inverse = 0;
    unsigned int result;
    *rangeLength = 0;
    if (inverseRangeLength) {
        *inverseRangeLength = 0;
    }

    ++*first;
    if (*first[0] == '^') {
        if (*first == last) {
            return ERR_PARSE_REGEX;
        }

        inverse = 1;
        ++*first;
    }

    if (*first[0] == ']') {
        if (*first == last) {
            return ERR_PARSE_REGEX;
        }
        
        if (inverse) {
            inverseRange[*inverseRangeLength] = (unsigned short)']';
            ++*inverseRangeLength;
        } else {
            range[*rangeLength] = (unsigned short)']';
            ++*rangeLength;
        } 
    }

    while (*first[0] != ']') {
        if (*first == last) {
            return ERR_PARSE_REGEX;
        }

        if (!parseBegin) {
            if (!lastSymbol) {
                return ERR_PARSE_REGEX;
            }

            result = utf8ToUnicode(first, last, &currentSymbol);
            if (result != REGEX_PARSE_OK) {
                return result;
            }

            while (currentSymbol != lastSymbol) {
                if (inverse) {
                    inverseRange[*inverseRangeLength] = currentSymbol;
                    ++*inverseRangeLength;
                } else {
                    range[*rangeLength] = currentSymbol;
                    ++*rangeLength;
                } 

                if (currentSymbol > lastSymbol) {
                    --currentSymbol;
                } else {
                    ++currentSymbol;
                }
            }
            parseBegin = 1;
        } else {
            if (*first[0] == '-') {
                parseBegin = 0;
                ++*first;
            } else {
                if (*first[0] != '%') {
                    result = utf8ToUnicode(first, last, &currentSymbol);
                    if (result != REGEX_PARSE_OK) {
                        return result;
                    }

                    if (inverse) {
                        inverseRange[*inverseRangeLength] = currentSymbol;
                        ++*inverseRangeLength;
                    } else {
                        range[*rangeLength] = currentSymbol;
                        ++*rangeLength;
                    } 
                    lastSymbol = currentSymbol;
                } else {
                    if (inverse) {
                        unsigned int result = readEscapedSymbol(first, last, inverseRangeLength, inverseRange);
                        if (result != REGEX_PARSE_OK) {
                            return result;
                        }
                    } else {
                        unsigned int result = readEscapedSymbol(first, last, rangeLength, range);
                        if (result != REGEX_PARSE_OK) {
                            return result;
                        }
                    }
                    lastSymbol = 0;
                }
            }
        } 
    }

    if (!parseBegin) {
        if (inverse) {
            inverseRange[*inverseRangeLength] = (unsigned short)'-';
            ++*inverseRangeLength;
        } else {
            range[*rangeLength] = (unsigned short)'-';
            ++*rangeLength;
        } 
    }

    ++*first;
    return REGEX_PARSE_OK;
}

static unsigned int readInternalRange(char *first,
                                      unsigned short *rangeLength,
                                      unsigned short *range) {
    unsigned int length = strlen(first);
    return readRange(&first, first + length - 1, rangeLength, range, NULL, NULL);
}

static unsigned int readInterval(char **first,
                                 char *last,
                                 unsigned short *low,
                                 unsigned short *high) {

    ++*first;
    unsigned char parseBegin = 1;
    char *numberBegin = *first;
    while (*first[0] != '}') {
        if (*first == last) {
            return ERR_PARSE_REGEX;
        }
        
        if (parseBegin) {    
            if (*first[0] == ',' && numberBegin != *first) {
                parseBegin = 0;
                *first[0] = '\0';
                *low = atoi(numberBegin);
                *first[0] = ',';
                numberBegin = *first + 1; 
            }  else if (*first[0] > '9' || *first[0] < 0) {
                return ERR_PARSE_REGEX;
            }
        } else if (*first[0] > '9' || *first[0] < 0) {
            return ERR_PARSE_REGEX;
        }

        ++*first;
    }

    if (numberBegin == *first) {
        *high = 0;
    } else {
        *first[0] = '\0';
        *high = atoi(numberBegin);
        *first[0] = '}';

        if (parseBegin) {
            *low = *high;  
        }
    } 

    if ((*high && *low > *high) || *high > MAX_INTERVAL) {
        return ERR_PARSE_REGEX;
    }

    ++*first;
    return REGEX_PARSE_OK;
}

static unsigned int readNextToken(char **first, 
                                  char *last, 
                                  token *nextToken) {
    unsigned int result = REGEX_PARSE_OK;
    if (*first >= last) {
        return REGEX_PARSE_END;
    }

    switch (*first[0]) {
        case '|':
            nextToken->type = REGEX_UNION;
            break;
        case '?':
            nextToken->type = REGEX_QUESTION;
            break;
        case '*':
            nextToken->type = REGEX_STAR;
            break;
        case '+':
            nextToken->type = REGEX_PLUS;
            break;
        case '(':
            nextToken->type = REGEX_REGEX;
            break;
        case ')':
            nextToken->type = REGEX_REGEX;
            result = REGEX_PARSE_END;
            break;
        case '[':
            nextToken->type = REGEX_SYMBOL;
            return readRange(first, last, &nextToken->symbolsLength, 
                                          (unsigned short *)&nextToken->symbols,
                                          &nextToken->inverseSymbolsLength, 
                                          (unsigned short *)&nextToken->inverseSymbols);
        case '{':
            nextToken->type = REGEX_INTERVAL;
            return readInterval(first, last, &nextToken->low, &nextToken->high);
        case '%':
            nextToken->type = REGEX_SYMBOL;
            return readEscapedSymbol(first, last, &nextToken->symbolsLength, (unsigned short *)&nextToken->symbols);
        case '.':
            nextToken->type = REGEX_SYMBOL;
            nextToken->symbolsLength = 1;
            nextToken->symbols[0] = REGEX_DOT;
            break;
        default:
            nextToken->type = REGEX_SYMBOL;
            nextToken->symbolsLength = 1;
            return utf8ToUnicode(first, last, &nextToken->symbols[0]);
    }

    ++*first;
    return result;
}

static unsigned int storeRegexStateMachine(ruleset *tree,
                                           unsigned short vocabularyLength, 
                                           unsigned short statesLength,
                                           char **newStateMachine, 
                                           unsigned int *stateMachineOffset) {

    unsigned int stateMachinelength = sizeof(unsigned short) * MAX_TRANSITIONS;
    stateMachinelength = stateMachinelength + sizeof(unsigned short) * statesLength * vocabularyLength;
    stateMachinelength = stateMachinelength + sizeof(unsigned char) * statesLength;
    if (!tree->regexStateMachinePool) {
        tree->regexStateMachinePool = malloc(stateMachinelength);
        if (!tree->regexStateMachinePool) {
            return ERR_OUT_OF_MEMORY;
        }

        memset(tree->regexStateMachinePool, 0, stateMachinelength);
        *stateMachineOffset = 0;
        *newStateMachine = &tree->regexStateMachinePool[0];
        tree->regexStateMachineOffset = 1;
    } else {
        tree->regexStateMachinePool = realloc(tree->regexStateMachinePool, tree->regexStateMachineOffset + stateMachinelength);
        if (!tree->regexStateMachinePool) {
            return ERR_OUT_OF_MEMORY;
        }

        memset(&tree->regexStateMachinePool[tree->regexStateMachineOffset], 0, stateMachinelength);
        *stateMachineOffset = tree->regexStateMachineOffset;
        *newStateMachine = &tree->regexStateMachinePool[tree->regexStateMachineOffset];
        tree->regexStateMachineOffset = tree->regexStateMachineOffset + stateMachinelength;
    }

    return RULES_OK;
}

static unsigned int createState(unsigned short *stateId, 
                                state **newState) {
    if (*stateId == MAX_STATES) {
        return ERR_REGEX_MAX_STATES;
    }
    *newState = malloc(sizeof(state));
    if (*newState == NULL) {
        return ERR_OUT_OF_MEMORY;
    }
    (*newState)->id = *stateId;
    (*newState)->transitionsLength = 0;
    (*newState)->refCount = 0;
    (*newState)->isAccept = 0;
    (*newState)->isReject = 0;
    (*newState)->hash = 0;
    ++*stateId;

    return RULES_OK;
}

static unsigned int linkStates(state *previousState, 
                               state *nextState, 
                               unsigned short tokenSymbol) {
    for (int i = 0; i < previousState->transitionsLength; ++i) {
        if (previousState->transitions[i].symbol == tokenSymbol && 
            previousState->transitions[i].next->id == nextState->id) {
            return RULES_OK;
        }
    }

    previousState->transitions[previousState->transitionsLength].symbol = tokenSymbol;
    previousState->transitions[previousState->transitionsLength].next = nextState;
    ++previousState->transitionsLength;
    ++nextState->refCount;
    if (previousState->transitionsLength == MAX_TRANSITIONS) {
        return ERR_REGEX_MAX_TRANSITIONS;
    }

    return RULES_OK;
}

static void deleteTransition(state *previousState, unsigned short index) {
    state *nextState = previousState->transitions[index].next;
    --nextState->refCount;
    if (!nextState->refCount) {
        free(nextState);
    }

    for (unsigned short i = index + 1; i < previousState->transitionsLength; ++i) {
        previousState->transitions[i - 1].symbol = previousState->transitions[i].symbol;
        previousState->transitions[i - 1].next = previousState->transitions[i].next;
    }
    --previousState->transitionsLength; 
}

static void unlinkStates(state *previousState, 
                         state *nextState, 
                         char tokenSymbol) {
    for (int i = 0; i < previousState->transitionsLength; ++i) {
        if (previousState->transitions[i].symbol == tokenSymbol && 
            previousState->transitions[i].next->id == nextState->id) {
            deleteTransition(previousState, i);
        }
    }
}

#ifdef _PRINT
static unsigned int printGraph(state *start) {
    CREATE_QUEUE(state*);
    unsigned char visited[MAX_STATES] = {0};
    state *currentState = start;        
    visited[currentState->id] = 1;
    while (currentState) {
        printf("State %d\n", currentState->id);
        if (currentState->isAccept) {
            printf("    Accept\n");
        }
        if (currentState->isReject) {
            printf("    Reject\n");
        }
        for (int i = 0; i < currentState->transitionsLength; ++ i) {
            transition *currentTransition = &currentState->transitions[i];
            printf("    transition %x to state %d\n", currentTransition->symbol, currentTransition->next->id);
            if (!visited[currentTransition->next->id]) {
                visited[currentTransition->next->id] = 1;
                ENQUEUE(currentTransition->next);
            }
        }

        DEQUEUE(&currentState);    
    }

    return RULES_OK;
}
#endif

static unsigned int cloneGraph(state *startState,
                               state *endState,
                               unsigned short *id,
                               state **newStart,
                               state **newEnd) {
    CREATE_QUEUE(state*);
    state *visited[MAX_STATES] = { NULL };
    state *currentState = startState;
    CREATE_STATE(id, &visited[currentState->id]);
    while (currentState) {
        if (currentState->isAccept) {
            visited[currentState->id]->isAccept = 1;
        }

        if (currentState->isReject) {
            visited[currentState->id]->isReject = 1;
        }

        for (int i = 0; i < currentState->transitionsLength; ++ i) {
            transition *currentTransition = &currentState->transitions[i];
            
            if (!visited[currentTransition->next->id]) {
                CREATE_STATE(id, &visited[currentTransition->next->id]);
                ENQUEUE(currentTransition->next);
            }

            LINK_STATES(visited[currentState->id], visited[currentTransition->next->id], currentTransition->symbol);
        }

        DEQUEUE(&currentState);    
    }

    *newStart = visited[startState->id];
    *newEnd = visited[endState->id];
    return RULES_OK;
}

static unsigned int createGraph(char **first, 
                                char *last, 
                                unsigned short *id, 
                                state **startState, 
                                state **endState) {
    CREATE_STATE(id, startState);
    CREATE_STATE(id, endState);
    state *previousState = *startState;
    state *currentState = *startState;

    token currentToken;
    unsigned int result = readNextToken(first, last, &currentToken);
    while (result == REGEX_PARSE_OK) {
        switch (currentToken.type) {
            case REGEX_SYMBOL:
                previousState = currentState;
                if (currentToken.symbolsLength) {
                    CREATE_STATE(id, &currentState);
                    for (unsigned short i = 0; i < currentToken.symbolsLength; ++i) {
                        LINK_STATES(previousState, currentState, currentToken.symbols[i]);
                    }
                } 

                if (currentToken.inverseSymbolsLength) {
                    CREATE_STATE(id, &currentState);
                    currentState->isReject = 1;
                    for (unsigned short i = 0; i < currentToken.inverseSymbolsLength; ++i) {
                        LINK_STATES(previousState, currentState, currentToken.inverseSymbols[i]);
                    }

                    CREATE_STATE(id, &currentState);
                    LINK_STATES(previousState, currentState, REGEX_DOT);    
                }                

                break;
            case REGEX_UNION:
                LINK_STATES(currentState, *endState, EMPTY);
                CREATE_STATE(id, &currentState);
                previousState = *startState;
                LINK_STATES(previousState, currentState, EMPTY);
                break;
            case REGEX_STAR:
                {
                    state *anchorState;
                    CREATE_STATE(id, &anchorState);
                    LINK_STATES(currentState, previousState, EMPTY);
                    LINK_STATES(currentState, anchorState, EMPTY);
                    LINK_STATES(previousState, anchorState, EMPTY);
                    previousState = currentState;
                    currentState = anchorState;
                }
                break;
            case REGEX_PLUS:
                {
                    state *anchorState;
                    CREATE_STATE(id, &anchorState);
                    LINK_STATES(currentState, previousState, EMPTY);
                    LINK_STATES(currentState, anchorState, EMPTY);
                    previousState = currentState;
                    currentState = anchorState;
                }
                break;
            case REGEX_QUESTION:
                {
                    state *anchorState;
                    CREATE_STATE(id, &anchorState);
                    LINK_STATES(currentState, anchorState, EMPTY);
                    LINK_STATES(previousState, anchorState, EMPTY);
                    previousState = currentState;
                    currentState = anchorState;
                }
                break;
            case REGEX_REGEX:
                {
                    state *subStart;
                    state *subEnd;
                    result = createGraph(first, last, id, &subStart, &subEnd);
                    if (result != REGEX_PARSE_OK) {
                        return result;
                    }
                    
                    LINK_STATES(currentState, subStart, EMPTY);
                    previousState = currentState;
                    currentState = subEnd;
                }
                break;
            case REGEX_INTERVAL: 
                {
                    state *newCurrent = NULL;
                    state *newPrevious = NULL;
                    state *subStart = previousState;
                    state *subEnd = currentState;
                    state *anchorState;
                    CREATE_STATE(id, &anchorState);
                    for (unsigned short i = 1; i < (!currentToken.high? currentToken.low: currentToken.high); ++i) {
                        result = cloneGraph(previousState, currentState, id, &subStart, &subEnd);
                        if (result != REGEX_PARSE_OK) {
                            return result;
                        }

                        if (newCurrent) {
                            LINK_STATES(newCurrent, subStart, EMPTY);
                        } else {
                            newPrevious = subStart;
                        }
                        
                        if (i >= currentToken.low) {
                            LINK_STATES(subStart, anchorState, EMPTY);
                        }

                        newCurrent = subEnd;
                    }

                    if (!currentToken.high) {
                        LINK_STATES(subEnd, subStart, EMPTY);
                    }
                     
                    if (!currentToken.low) {
                        LINK_STATES(previousState, anchorState, EMPTY);
                    }

                    if (!newPrevious) {
                        LINK_STATES(currentState, anchorState, EMPTY);
                        previousState = currentState;
                    } else {
                        LINK_STATES(currentState, newPrevious, EMPTY); 
                        LINK_STATES(newCurrent, anchorState, EMPTY); 
                        previousState = newCurrent;
                    } 
                    currentState = anchorState;     
                }
                break;
        }
        if (result == REGEX_PARSE_OK) {
            result = readNextToken(first, last, &currentToken);
        }
    }

    LINK_STATES(currentState, *endState, EMPTY);

    if (result == REGEX_PARSE_END) {
        return REGEX_PARSE_OK;
    }

    return result;
}

static unsigned int validateGraph(char **first, char *last) {
    token currentToken;
    unsigned int result = readNextToken(first, last, &currentToken);
    while (result == REGEX_PARSE_OK) {
        switch (currentToken.type) {
            case REGEX_SYMBOL:
            case REGEX_UNION:
            case REGEX_STAR:
            case REGEX_PLUS:
            case REGEX_QUESTION:
                break;
            case REGEX_REGEX:
                result = validateGraph(first, last);
                if (result != REGEX_PARSE_OK) {
                    return result;
                }
                    
                break;
        }

        if (result == REGEX_PARSE_OK) {
            result = readNextToken(first, last, &currentToken);
        }
    }

    if (result == REGEX_PARSE_END) {
        return REGEX_PARSE_OK;
    }

    return REGEX_PARSE_OK;
}

static unsigned short calculateHash(state **list, 
                                    unsigned short stateListLength) {
    unsigned int hash = 5381;
    for (unsigned short i = 0; i < stateListLength; ++i) {
        hash = ((hash << 5) + hash) + list[i]->id;
    }   

    return hash;
}

static unsigned int ensureState(unsigned short *id, 
                                state **list, 
                                unsigned short stateListLength, 
                                state **newState) {
    CREATE_STATE(id, newState);
    for (unsigned short i = 0; i < stateListLength; ++i) {
        state *targetState = list[i];
        for (unsigned short ii = 0; ii < targetState->transitionsLength; ++ii) {
            transition *targetTransition = &targetState->transitions[ii];
            LINK_STATES(*newState, targetTransition->next, targetTransition->symbol);
        }

        if (targetState->isAccept) {
            (*newState)->isAccept = 1;
        }

        if (targetState->isReject) {
            (*newState)->isReject = 1;
        }

        if ((*newState)->isReject && (*newState)->isAccept) {
            return ERR_REGEX_CONFLICT;
        }        
    }

    return RULES_OK;
}

static unsigned int consolidateStates(state *currentState, 
                                      unsigned short *id) {
    for (unsigned short i = 0; i < currentState->transitionsLength; ++i) {
        transition *currentTransition = &currentState->transitions[i];
        if (!currentTransition->symbol) {
            state *nextState = currentTransition->next;
            if (nextState != currentState) {
                for (unsigned short ii = 0; ii < nextState->transitionsLength; ++ii) {
                    transition *nextTransition = &nextState->transitions[ii];
                    LINK_STATES(currentState, nextTransition->next, nextTransition->symbol);
                    if (nextState->refCount == 1) {
                        --nextTransition->next->refCount;
                    }
                }
            }

            if (nextState->isAccept) {
                currentState->isAccept = 1;
            }

            if (nextState->isReject) {
                currentState->isReject = 1;
            }

            if (currentState->isAccept && currentState->isReject) {
                return ERR_REGEX_CONFLICT;
            }

            deleteTransition(currentState, i);
            --i;
        }
    }

    return RULES_OK;
}

static unsigned int consolidateTransitions(state *currentState, 
                                           unsigned short *id, 
                                           state **set) {
    transition oldTransitions[MAX_TRANSITIONS];
    unsigned short oldTransitionsLength = 0;
    transition newTransitions[MAX_TRANSITIONS];
    unsigned short newTransitionsLength = 0;
    unsigned char visited[MAX_TRANSITIONS] = {0};

    for (unsigned short i = 0; i < currentState->transitionsLength; ++i) {
        transition *currentTransition = &currentState->transitions[i];
        CREATE_LIST(state*);
        unsigned short foundSymbol = 0;
        if (!visited[(unsigned short)currentTransition->symbol]) {
            visited[(unsigned short)currentTransition->symbol] = 1;
            for (unsigned short ii = i + 1; ii < currentState->transitionsLength; ++ ii) {
                transition *targetTransition = &currentState->transitions[ii];
                if ((currentTransition->symbol == targetTransition->symbol) ||
                    (currentTransition->symbol == REGEX_DOT && !targetTransition->next->isReject) ||
                    (targetTransition->symbol == REGEX_DOT && !currentTransition->next->isReject)) {
                    foundSymbol = currentTransition->symbol;
                    if (foundSymbol == REGEX_DOT) {
                        foundSymbol = targetTransition->symbol;
                    }
                    
                    if (LIST_EMPTY()) {
                        ADD(currentTransition->next);
                        oldTransitions[oldTransitionsLength].symbol = currentTransition->symbol;
                        oldTransitions[oldTransitionsLength].next = currentTransition->next;
                        ++oldTransitionsLength;
                    }

                    ADD(targetTransition->next);
                    oldTransitions[oldTransitionsLength].symbol = targetTransition->symbol;
                    oldTransitions[oldTransitionsLength].next = targetTransition->next;
                    ++oldTransitionsLength;
                }
            }

            if (!LIST_EMPTY()) {
                state *newState;
                unsigned int newStateHash = calculateHash(LIST);
                HGET(newStateHash, &newState);
                if (!newState) {
                    unsigned int result = ensureState(id, LIST, &newState);
                    if (result != REGEX_PARSE_OK) {
                        return result;
                    }

                    newState->hash = newStateHash;
                    HSET(newState);
                } 

                newTransitions[newTransitionsLength].symbol = foundSymbol;
                newTransitions[newTransitionsLength].next = newState;
                ++newTransitionsLength;
            }
        }
    }

    for (unsigned short i = 0; i < oldTransitionsLength; ++i) {
        unlinkStates(currentState, oldTransitions[i].next, oldTransitions[i].symbol);
    }

    for (unsigned short i = 0; i < newTransitionsLength; ++i) {
        LINK_STATES(currentState, newTransitions[i].next, newTransitions[i].symbol);
    }

    return RULES_OK;
}

static unsigned int transformToDFA(state *nfa, 
                                   unsigned short *id) {

#ifdef _PRINT
    printf("*** NFA ***\n");
    printGraph(nfa);
#endif

    CREATE_HASHSET(state*);
    CREATE_QUEUE(state*);
    unsigned char visited[MAX_STATES] = {0};
    state *currentState = nfa;
    visited[currentState->id] = 1;
    while (currentState) {
        unsigned int result = consolidateStates(currentState, id);
        if (result != RULES_OK) {
            return result;
        }

        result = consolidateTransitions(currentState, id, HASHSET);
        if (result != REGEX_PARSE_OK) {
            return result;
        }
        
        for (int i = 0; i < currentState->transitionsLength; ++ i) {
            transition *currentTransition = &currentState->transitions[i];
            if (!visited[currentTransition->next->id]) {
                visited[currentTransition->next->id] = 1;
                ENQUEUE(currentTransition->next);
            }
        }

        DEQUEUE(&currentState);    
    }

#ifdef _PRINT
    printf("*** DFA ***\n");
    printGraph(nfa);
#endif

    return RULES_OK;
}

static unsigned int calculateGraphDimensions(state *start, 
                                        unsigned short *vocabularyLength, 
                                        unsigned short *statesLength) {
    *vocabularyLength = 0;
    *statesLength = 0;
    CREATE_QUEUE(state*);
    unsigned char visited[MAX_STATES] = {0};
    unsigned char vocabulary[MAX_TRANSITIONS] = {0};
    state *currentState = start;
    visited[currentState->id] = 1;
    while (currentState) {
        ++*statesLength;
        for (int i = 0; i < currentState->transitionsLength; ++ i) {
            transition *currentTransition = &currentState->transitions[i];
            if (!vocabulary[(unsigned short)currentTransition->symbol]) {
                vocabulary[(unsigned short)currentTransition->symbol] = 1;
                ++*vocabularyLength;
            }

            if (!visited[currentTransition->next->id]) {
                visited[currentTransition->next->id] = 1;
                ENQUEUE(currentTransition->next);
            }
        }

        DEQUEUE(&currentState);    
    }

    return RULES_OK;

}

static unsigned int packGraph(state *start, 
                              char *stateMachine,
                              unsigned short vocabularyLength,
                              unsigned short statesLength) {

    CREATE_QUEUE(state*);
    unsigned short visited[MAX_STATES] = {0};
    unsigned short *vocabulary = (unsigned short *)stateMachine;
    unsigned short *stateTable = (unsigned short *)(stateMachine + MAX_TRANSITIONS * sizeof(unsigned short));
    unsigned char *acceptVector = (unsigned char *)(stateTable + (vocabularyLength * statesLength));
    unsigned short stateNumber = 1;
    unsigned short vocabularyNumber = 1;
    state *currentState = start;
    visited[currentState->id] = stateNumber;
    ++stateNumber;
    while (currentState) {
        unsigned short targetStateNumber = visited[currentState->id];
        if (currentState->isAccept) {
            acceptVector[targetStateNumber - 1] = 1;
        }

        for (int i = 0; i < currentState->transitionsLength; ++ i) {
            transition *currentTransition = &currentState->transitions[i];
            if (!vocabulary[currentTransition->symbol]) {
                vocabulary[currentTransition->symbol] = vocabularyNumber;
                ++vocabularyNumber;
            }

            if (!visited[currentTransition->next->id]) {
                visited[currentTransition->next->id] = stateNumber;
                ++stateNumber;
                ENQUEUE(currentTransition->next);
            }

            unsigned short targetSymbolNumber = vocabulary[currentTransition->symbol];
            stateTable[statesLength * (targetSymbolNumber - 1) + (targetStateNumber - 1)] = visited[currentTransition->next->id];
        }

        DEQUEUE(&currentState);    
    }

    return RULES_OK;
}

unsigned int validateRegex(char *first, 
                           char *last) {
    return validateGraph(&first, last);
}

unsigned int compileRegex(void *tree, 
                          char *first, 
                          char *last, 
                          unsigned short *vocabularyLength,
                          unsigned short *statesLength,
                          unsigned int *regexStateMachineOffset) {
    state *start;
    state *end;
    unsigned short id = 0;
    unsigned int result = createGraph(&first, last, &id, &start, &end);
    if (result != RULES_OK) {
        return result;
    }
    end->isAccept = 1;
    ++start->refCount;
    result = transformToDFA(start, &id);
    if (result != RULES_OK) {
        return result;
    }
    result = calculateGraphDimensions(start, 
                                 vocabularyLength, 
                                 statesLength);
    if (result != RULES_OK) {
        return result;
    }
    char *newStateMachine;    
    result = storeRegexStateMachine((ruleset *)tree, 
                                    *vocabularyLength, 
                                    *statesLength,
                                    &newStateMachine,
                                    regexStateMachineOffset);
    if (result != RULES_OK) {
        return result;
    }
    return packGraph(start, 
                     newStateMachine, 
                     *vocabularyLength,
                     *statesLength);
}

unsigned char evaluateRegex(void *tree,
                            char *first,
                            unsigned short length, 
                            unsigned short vocabularyLength,
                            unsigned short statesLength,
                            unsigned int regexStateMachineOffset) {
    unsigned short *vocabulary = (unsigned short *)&((ruleset *)tree)->regexStateMachinePool[regexStateMachineOffset];
    unsigned short *stateTable = (unsigned short *)(vocabulary + MAX_TRANSITIONS);
    unsigned char *acceptVector = (unsigned char *)(stateTable + (vocabularyLength * statesLength));
    unsigned short currentState = 1;
    char *last = first + length;
    while (first < last) {
        unsigned short unicodeSymbol;
        if (utf8ToUnicode(&first, last, &unicodeSymbol) != REGEX_PARSE_OK) {
            return 0;
        } else {
            unsigned short currentSymbol = vocabulary[unicodeSymbol];
            if (!currentSymbol) {
                currentSymbol = vocabulary[REGEX_DOT];
                if (!currentSymbol) {
                    return 0;
                }

                currentState = stateTable[statesLength * (currentSymbol - 1) + (currentState - 1)];
                if (!currentState) {
                    return 0;
                }
            } else {
                currentState = stateTable[statesLength * (currentSymbol - 1) + (currentState - 1)];
                if (!currentState) {
                    currentSymbol = vocabulary[REGEX_DOT];
                    if (!currentSymbol) {
                        return 0;
                    }

                    currentState = stateTable[statesLength * (currentSymbol - 1) + (currentState - 1)];
                    if (!currentState) {
                        return 0;
                    }
                }
            }
        }
    }
    
    return acceptVector[currentState - 1];
}
