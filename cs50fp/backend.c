#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const int dataset_size = 2477; // known size of the csv
const int hashtable_size = (int) (dataset_size / 0.75); // setting constant hash table size based

typedef struct vocab_entry {
    char word[20]; // What would max length of a word be?
    int valence;
    struct vocab_entry* next; // check syntax
} vocab_entry;

float SA_valence(char* text, vocab_entry dataset[]); // sentimen analysis valence func
// other SA function
int hash_func(char* word); // hash function

// need to get target text(s) in here

int main() 
{
    FILE *file = fopen("Afinn.csv", "r");
    if (file == NULL) {
        fprint("Failure opening the file\n");
        return 1;
    }

    // Update to the new reality of hash table
    vocab_entry hash_table[hashtable_size]; // creating hash table
    char buffer[23]; // to store each line
    int i = 0; // keeps track of line number

    while(fgets(buffer, sizeof(buffer), file))
    {
        // implementing hash table
        if (i >= dataset_size)
        {
            break;
        }

        char* word = strtok(buffer, ","); // copies part of string before comma
        if (word != NULL)
        {
            char* number = strtok(NULL, "\n"); // copies the number part as string
            if (number != NULL)
            {
                int hash = hash_func(word)
                // use while loop
                // check if the current vocab_entry *next is NULL
                // once it is, create next entry, set empty pointer ot it
                if (hash_table[hash].next = NULL)
                {
                    // the code is not fully corect
                    strcopy(hash_table[hash].word, word);
                    hash_table[hash].valence = number;
                    // hash_table[hash].next = pointer?
                }
                else
                {
                    // follow the pointer and check again
                }
            }
        }
        i++
    }

    int valence = SA_valence(text, dataset);

    return 0;
}

float SA_valence(char* text, vocab_entry dataset[])
{

    // mind the length of words in dataset

    int length = len(dataset);
    int total = 0;

    const char* delimiters = " '\",.;:!-()#@*$[]{}\%" // check espace syntax

    // get total valence

    // return total valence / i;
}

int hash_func(char* word);
{
    // credit this hash func, Polynomial Accumulation
    unsigned int hash = 0;
    int c;
    while ((c = *word++)) // understand this better. Why the look stops?
    {
        hash = hash * 33 + c;
    }
    return hash % hashtable_size;
}