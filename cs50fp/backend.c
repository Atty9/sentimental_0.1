#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const int dataset_size = 2477; // known size of the csv
const int hashtable_size = (int) (dataset_size / 0.75); // setting constant hash table size
char* text = "This company isn't good, I don't like it, it deceives, lies. Stock bad"; // placeholder text

typedef struct node {
    char word[100]; 
    int valence;
    struct node* next; // syntax?
} node;

void nullifier(node* hash_table[], int size);
int table_filler(node* hash_table[], FILE* file);
float valence_analyzer(char* text, node* dataset[]);
int hash_func(char* word);

int main(void) 
{
    // Opening the dataset csv
    FILE *file = fopen("Afinn.csv", "r");
    if (file == NULL) {
        printf("Failure opening the file\n");
        return 1;
    }

    // Creating hash table
    node* hash_table[hashtable_size];
    // Setting pointers to NULL
    nullifier(hash_table, hashtable_size);
    // Filling hash table with data from csv 
    table_filler(hash_table, file); // what to do with returns? 
    
    // Getting the average valence of a text
    float avg_valence = valence_analyzer(text, hash_table);
    printf("Valence = %f", avg_valence);

    fclose(file);

    return 0;
}

void nullifier(node* hash_table[], int size)
{
    // sets hash_table pointers to NULL
    for (int i = 0; i < size; i++)
    {
        hash_table[i] = NULL;
    }
}

int table_filler(node* hash_table[], FILE* file) // mind access to the text
{
    /* Takes hash table and file as input.
    Fills the table with data from the file (assumes csv) */

    char buffer[100]; // stores line's contents
    int i = 0; // stores line number

    // Managing the first line of the csv
    
    if (fgets(buffer, sizeof(buffer), file) == NULL)
    {
        printf("CSV is empty or unexpected error reading the first line. Closing\n");
        return 1;
    }
    i += 1; // needed to account for the first line?
    // Reading the rest of csv line by line, copying data to the hashtable
    while(fgets(buffer, sizeof(buffer), file)) // What about the title line of the csv?
    {

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
                unsigned int hash = hash_func(word);
                node* cursor = hash_table[hash];
                while (cursor != NULL)
                {
                    cursor = cursor -> next;
                }
                strcpy(cursor -> word, word);
                cursor -> valence = atoi(number); // syntax?
                cursor -> next = NULL;
            }
        }
        i++;
    }
    return 0;
}

float valence_analyzer(char* text, node* hash_table[])
{
    /* Takes a text as string and dictionary of words and corresponding valences as inputs.
    Returns averange valence of text as a float between -5 and 5 */

    int total = 0;
    const char* delimiters = " '\",.;:!-()#%@*$[]{}\n";
    char* word = strtok(text, delimiters);

    // Check valence of the 1st word in the text
    node* cursor = hash_table[hash_func(word)];
    while (cursor != NULL)
    {
        cursor = cursor -> next;
    }
    total += cursor->valence;

    // Loop through the rest, getting all the valences
    while ((word = strtok(NULL, delimiters)))
    {
        cursor = hash_table[hash_func(word)];
        while (cursor != NULL)
        {
            cursor = cursor -> next;
        }
        total += cursor->valence;
    }
    
    // return the average valence of the text
    return total / hashtable_size;
}

int hash_func(char* word)
{
    // Takes a string, returns a hash (int)

    // credit this hash func, Polynomial Accumulation
    unsigned int hash = 0;
    int c;
    while ((c = *(word++))) // while (*(word++)) also works, but we use c to dereference only once per loop
    {
        hash = hash * 33 + c;
    }
    return hash % hashtable_size;
}