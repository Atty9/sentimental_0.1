#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Valgrind cleared
// Thread safety concern?
// verify input is strings?

const int dataset_size = 2478; // known size of the dataset
const int hashtable_size = (int) (dataset_size / 0.75); // setting constant hash table size
// char text[] = "This company isn't good, I good abandon giga mate friend youtful zealot don't like it, it deceives, lies. Stock bad\n"; // placeholder text
// char text[];

typedef struct node {
    char word[100]; 
    int valence;
    struct node* next;
} node;

void nullifier(node* hash_table[], int size);
void to_lower_case(char* string);
int table_filler(node* hash_table[], FILE* file);
int valence_analyzer(char* text, node* dataset[], float* result);
int hash_func(char* string);
void memory_cleaner(node* hash_table[]);
void cleaner2(node* curent_node);

int main(int argc, char* argv[]) 
{
    // Verifying correct usage
    if (argc < 2)
    {
        fprintf(stderr, "Usage: %s str1, str2, ...\n", argv[0]);
        return 1;
    }

    // Opening the dataset csv
    FILE *file = fopen("Afinn.csv", "r");
    if (file == NULL) {
        fprintf(stderr, "Failure opening Afinn.csv\n");
        return 2;
    }

    // Creating hash table
    node* hash_table[hashtable_size];

    // Setting pointers to NULL
    nullifier(hash_table, hashtable_size);
    
    // Filling hash table with data from csv 
    if (table_filler(hash_table, file) != 0)
    {
        fprintf(stderr, "Error in hash table filler function\n");
        return 3;
    }
    
    // Getting the average valence of each input text
    float result[argc - 1];
    int k = 0;
    for (int i = 1; i < argc; i++)
    {
        if (valence_analyzer(argv[i], hash_table, &result[k]) == 0)
        {
            printf("Valence of the text #%d: %f\n", i, result[k]);
        }
        else
        {
            fprintf(stderr, "No data in valence analyzer function for text #%d\n", i);
            // return 4;
        }
        k++;
    }

    // Closing files, clearing memory allocations
    fclose(file);
    memory_cleaner(hash_table);

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

void to_lower_case(char* string)
{
    // converts string to all lowercase
    while (*string)
    {
        *string = tolower((unsigned char) *string);
        string++;
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
        return 1;
    }

    // Reading the rest of csv line by line, copying data to the hashtable
    while(fgets(buffer, sizeof(buffer), file)) // What about the title line of the csv?
    {

        if (i >= dataset_size)
        {
            break;
        }

        char* string = strtok(buffer, ","); // copies part of string before comma
        if (string != NULL)
        {
            char* number = strtok(NULL, "\n"); // copies the number part as string
            if (number != NULL)
            {
                to_lower_case(string);

                // Navigating towards the last node of the ll
                unsigned int hash = hash_func(string);
                node* cursor = hash_table[hash]; 
                node* previous = NULL;
                while (cursor != NULL) 
                {
                    previous = cursor;
                    cursor = cursor -> next; 
                }

                // Creating new node in the linked list
                cursor = malloc(sizeof(node));
                if (cursor == NULL)
                {
                    return 2;
                }

                // Filling the new node
                strcpy(cursor -> word, string);
                cursor -> valence = atoi(number);
                cursor -> next = NULL;

                // Handling case of empty bucket vs non-empty
                if (previous == NULL)
                {
                    hash_table[hash] = cursor;
                }
                else
                {
                    previous->next = cursor;
                }
            }
        }
        i++;
    }
    return 0;
}

int valence_analyzer(char* text, node* hash_table[], float* result)
{
    /* Takes a text as string and dictionary of words and corresponding valences as inputs.
    Returns averange valence of text as a float between -5 and 5 */

    int total = 0;
    int count = 0;
    const char* delimiters = " \",.;:!-()#%@*$[]{}\n"; // omitting ' for now


    // Check valence of the 1st word in the text
    char* string = strtok(text, delimiters);
    to_lower_case(string);
    node* cursor = hash_table[hash_func(string)];
    while (cursor != NULL)
    {
        if (strcmp(cursor->word, string) == 0)
        {
            total += cursor->valence;
            count++;
            break;
        }
        cursor = cursor -> next;   
    } // codespace is unhappy if this comment is not here

    // Loop through the rest, getting all the valences
    while ((string = strtok(NULL, delimiters)))
    {
        to_lower_case(string);

        cursor = hash_table[hash_func(string)];
        while (cursor != NULL)
        {
            
            if (strcmp(cursor->word, string) == 0)
            {
                total += cursor->valence;
                count++;
                printf("cursor's string: %s\n", cursor->word); // temp
                printf("cursor's number: %d\n", cursor->valence); // temp
                printf("Total: %d, Count: %d\n", total, count); // temp
                break;
            }
            cursor = cursor -> next;   
        }
    }
    
    // Accounting for 0 division
    if (count == 0)
    {
        return 1;
    }

    // Returning the average valence of the text
    printf("Total: %d, Count: %d\n", total, count); //temp
    *result = (float) total / count;
    return 0;
}

int hash_func(char* string)
{
    // Takes a string, returns a hash (int)

    // credit this hash func, Polynomial Accumulation

    unsigned int hash = 0;
    int c;
    while ((c = *(string++))) // while (*(word++)) also works, but we use c to dereference only once per loop
    {
        hash = hash * 33 + c;
    }
    return hash % hashtable_size;
}

void memory_cleaner(node* hash_table[])
{
    // Clears buckets of the hash table
    for (int i = 0; i < hashtable_size; i++)
    {
        cleaner2(hash_table[i]);
    }
}

void cleaner2(node* cur_node)
{
    // Frees allocated memory of a linked list recursively
    if (cur_node == NULL)
    {
        return;
    }
    cleaner2(cur_node->next);
    free(cur_node);
    return;
}