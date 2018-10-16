#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_CONTACTS 16

struct contact {
    char *name;
    char *bio;
};

struct contact *contacts[MAX_CONTACTS];
unsigned int num_contacts = 0;

void print_contacts(){
    for (int i = 0; i < num_contacts; i++){
        if (contacts[i]->bio != NULL){
            printf("%s - %s\n", contacts[i]->name, contacts[i]->bio);
        }else{
            printf("%s - (No bio)\n", contacts[i]->name);
        }
    }
}

struct contact *find_contact(char *name){
    for (int i = 0; i < num_contacts; i++){
        if (!strcmp(name, contacts[i]->name)){
            return contacts[i];
        }
    }
    return NULL;
}

void create_contact(char *name){
    if (num_contacts == MAX_CONTACTS){
        puts("Too many contacts! Delete one first!");
        return;
    }

    struct contact *contact = (struct contact *)malloc(sizeof(struct contact));
    if (contact == NULL){
        puts("Could not allocate new contact.");
        exit(-1);
    };

    /* make a copy of the name on the heap */
    contact->name = strdup(name);
    if (contact->name == NULL){
        puts("Could not duplicate name.");
        exit(-1);
    }

    contacts[num_contacts++] = contact;
}

void delete_contact(struct contact *contact){
    free(contact->name);

    /* if the bio is set, free it as well */
    if (contact->bio != NULL){
        free(contact->bio);
    }

    free(contact);

    /* replace the corresponding index with the last contact and decrement num_contacts */
    for (int i = 0; i < num_contacts; i++){
        if (contacts[i] == contact){
            contacts[i] = contacts[num_contacts - 1];
            num_contacts--;
            break;
        }
    }
}

void set_bio(struct contact *contact){
    char input[4];
    size_t length;

    /* we'll replace the old bio */
    if (contact->bio != NULL){
        free(contact->bio);
    }

    puts("How long will the bio be?");
    if (fgets(input, 4, stdin) == NULL){
        puts("Couldn't read length.");
        return;
    };

    length = strtoul(input, NULL, 10);
    if (length > 255){
        puts("Bio must be at most 255 characters.");
        return;
    }

    contact->bio = (char *)malloc(length+1);
    if (contact->bio == NULL){
        puts("Couldn't allocate bio.");
        exit(-1);
    }

    puts("Enter your new bio:");
    if (fgets(contact->bio, length+1, stdin) == NULL){
        puts("Couldn't read bio.");
        return;
    }

    puts("Bio recorded.");
}

void menu(){
    puts("Available commands:");
    puts("\tdisplay - display the contacts");
    puts("\tcreate [name] - create a new contact");
    puts("\tdelete [name] - delete an existing contact");
    puts("\tbio [name] - set the bio for an existing contact");
    puts("\tquit - exit the program");
}

int process_cmd(char *cmd){
    struct contact *contact;
    char *name;

    if (!strncmp(cmd, "display", 7)){
        print_contacts();

    }else if (!strncmp(cmd, "create", 6)){
        name = strtok(&cmd[7], "\n");
        if (name == NULL){
            puts("Invalid command");
            return 0;
        }

        create_contact(name);
        printf("Created contact \"%s\"\n", name);

    }else if (!strncmp(cmd, "delete", 6)){
        name = strtok(&cmd[7], "\n");
        if (name == NULL){
            puts("Invalid command");
            return 0;
        }

        contact = find_contact(name);
        if (contact == NULL){
            puts("Can't find contact");
            return 0;
        }

        delete_contact(contact);
        printf("Deleted contact \"%s\"\n", name);

    }else if (!strncmp(cmd, "bio", 3)){
        name = strtok(&cmd[4], "\n");
        if (name == NULL){
            puts("Invalid command");
            return 0;
        }

        contact = find_contact(name);
        if (contact == NULL){
            puts("Can't find contact");
            return 0;
        }

        set_bio(contact);

    }else if (!strncmp(cmd, "quit", 4)){
        return 1;
    }else{
        puts("Invalid option");
        menu();
    }
    return 0;
}

void command_loop(){
    char buf[512];

    menu();
    while(1){
        puts("\nEnter your command:");
        putchar('>'); putchar(' ');

        if(fgets(buf, 512, stdin) == NULL)
            break;

        if (process_cmd(buf)){
            return;
        }
    }
}

int main(int argc, char **argv){
    /* Don't buffer stdout. */
    setbuf(stdout, NULL);

    command_loop();
}
