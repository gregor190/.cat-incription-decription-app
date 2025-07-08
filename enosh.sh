#!/bin/bash

# Input: name of file or folder
INPUT="$1"
PASSWORD="meow_subuntu_power"
PASSWORD_A="12344321"
PASSWORD_B="12344132"

if [ -z "$INPUT" ]; then
    echo "Usage: $0 <file_or_folder>"
    exit 1
fi

# Step 1: tar.gz
tar -czf layer1.tar.gz "$INPUT"

# Step 2: gpg encrypt without prompt
echo "$PASSWORD" | gpg --batch --yes --passphrase-fd 0 -c layer1.tar.gz

# Step 3: Layer 2
tar -czf layer2.tar.gz layer1.tar.gz.gpg
echo "$PASSWORD_A" | gpg --batch --yes --passphrase-fd 0 -c layer2.tar.gz

# Step 4: Layer 3
tar -czf layer3.tar.gz layer2.tar.gz.gpg
echo "$PASSWORD_B" | gpg --batch --yes --passphrase-fd 0 -c layer3.tar.gz

# Final output
mv layer3.tar.gz.gpg "$INPUT.tar.gz.gpg"

# Cleanup
rm -f layer1.tar.gz layer1.tar.gz.gpg
rm -f layer2.tar.gz layer2.tar.gz.gpg
rm -f layer3.tar.gz

echo "Triple-layered tar.gz.gpg file created: $INPUT.tar.gz.gpg"
