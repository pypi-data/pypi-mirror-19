# FLask-Stormpath-Plus

## What is the differencies between plus and original version

- add a sha256 hashing to the password before sending to stormpath server.

## Why

This is a little tricky.

I think send the password directly without hashing to stormpath is not good,
So I add a simple function to hash the password before sending it to stormpath.

It use the app's `SECRET-KEY` as the salt for the encryption.