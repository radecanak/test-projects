#!/bin/bash
dir=$1
filter="*.*"

show_help() {
cat << EOF
Usage: ${0##*/} dir [--filter=?]
EOF
}

case $1 in
   -h|-\?|--help)   # Call a "show_help" function to display, then exit.
            show_help
            exit
            ;;
    esac
  
case $2 in
        --filter=?*)       # Takes an option argument, ensuring it has been specified.
            filter=${2#*=} # Delete everything up to "=" and assign the remainder.
            if [ "${filter:0:1}" = "." ]
            then 
                filter="*$filter"
            fi
            ;;
        "")
            ;;
        *)               # Default case.
            show_help
            exit
            ;;
    esac 
    
filter="$1/$filter"
ls $filter