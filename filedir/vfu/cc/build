#!/bin/sh

echo "Compiling VSLIB..."
cd vslib
make
if [ -e libvslib.a ]; then
  echo "VSLIB compiled ok."
else
  echo "VSLIB compilation failed..."
fi

cd ..

echo "Compiling VFU..."
cd vfu
make
if [ -e vfu ]; then
  echo "VFU compiled ok."
else
  echo "VFU compilation failed..."
fi

cd ..
 
