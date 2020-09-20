# Countdown-Word-Anagram-Solver
A solver for anagrams giving solutions of varying lengths. Inspired by the Channel 4 show Countdown.

To run this program you will need an API key from Merriam Webster which is free and simple to obtain. You will then need to save this key in the config.py file.

### Instructions
1) When you run this program you will be asked to enter in a word that you would like to find the anagrams for. Enter this in here.

#### Options:

1) You can enter in only the word and it will find anagrams of that same length, or
2) You can enter in a word and then enter a number after a space (min: 3, max: length of word) which will find anagrams of that length, or
3) You can enter in a word and then enter "all" after a space which will find solutions of all lengths starting with the length of the word.

## Importing the File
Alternatively to the above, in order to use this functionality in your own program, you can instead import the functions into your own program:

    from CountdownChecker import countdown

Then use the following:

    countdown("vegdances") #use all letters
    countdown("vegdances 7") #use 7 letters

Output:

    {'scavenged'}
    {'avenged', 'encased', 'avenges'}

The options available to you when importing are the first two in the list above under Options.