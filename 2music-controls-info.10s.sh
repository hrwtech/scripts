#!/bin/bash

# Shows infos on artist, album, track and more in cmus or pianobar.
#
# Special thanks to Google for providing the open-source icons: https://github.com/google/material-design-icons
# and to mcchrish and alekseysotnikov for their helpful existing BitBar scripts
#
# metadata
# <bitbar.title>Music Controls - Next Track Button</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Sebastián Barschkis</bitbar.author>
# <bitbar.author.github>sebbas</bitbar.author.github>
# <bitbar.desc>Plays the next track in cmus, iTunes, Music, Spotify or pianobar.</bitbar.desc>
# <bitbar.dependencies>perl</bitbar.dependencies>
# <bitbar.image>https://raw.githubusercontent.com/sebbas/music-controls-bitbar/master/music-controls-screenshot.png</bitbar.image>
# <bitbar.abouturl>http://github.com/sebbas/music-controls-bitbar</bitbar.abouturl>

# export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
# export LC_CTYPE="UTF-8"

# pianobar_ctlfile="$HOME/.config/pianobar/ctl"
# pianobar_stationsfile="$HOME/.config/pianobar/stations"
# pianobar_playingfile="$HOME/.config/pianobar/playing"
cmus_cachefile="$HOME/.config/cmus/cache"

display_length=40

# Enables features that are still under development
EXPERIMENTAL_MODE=0

NONE="none"
CMUS="cmus"
ITUNES="iTunes"
MUSIC="Music"
SPOTIFY="Spotify"
PIANOBAR="pianobar"

list_icon_light=""

note_icon_light=""
note_icon_dark=""

person_icon_light=""

album_icon_light=""
album_icon_dark=""

station_icon_light=""
station_icon_dark=""

star_icon_light=""

# Trigger next action in library section (e.g. play track in cmus)
if [[ "$1" = 'cmus_song' ]]; then
  f=$(echo -e "player-play $2")
  cmus-remote -C "$f"
  exit
fi
if [[ "$1" = 'itunes_next' ]]; then
  osascript -e 'tell application "iTunes" to next track'
  exit
fi
if [[ "$1" = 'music_next' ]]; then
  osascript -e 'tell application "Music" to next track'
  exit
fi

# Get pid of music apps to see if they are currently running
cmus_pid=$(pgrep -x "$CMUS")
itunes_pid=$(pgrep -x "$ITUNES")
music_pid=$(pgrep -x "$MUSIC")
spotify_pid=$(pgrep -x "$SPOTIFY")
pianobar_pid=$(pgrep -x "$PIANOBAR")

# Keep track of music source
# Reorder items in for -loop to your liking to change order of precendece
# (i.e. if available, left-most audio source will be used first)
for s in "$CMUS" "$ITUNES" "$MUSIC" "$SPOTIFY" "$PIANOBAR"; do
  if [[ $s = "$CMUS" && $cmus_pid ]]; then
    current_source="$CMUS"
    break
  elif [[ $s = "$ITUNES" && $itunes_pid ]]; then
    current_source="$ITUNES"
    break
  elif [[ $s = "$MUSIC" && $music_pid ]]; then
    current_source="$MUSIC"
    break
  elif [[ $s = "$SPOTIFY" && $spotify_pid ]]; then
    current_source="$SPOTIFY"
    break
  fi
done

# Do not display menu icon if no audio source is active
if [[ $current_source = "$NONE" ]]; then
  exit
fi

function playing_info
{
  if [[ $current_source = "$CMUS" ]]; then
    track=$(cmus-remote -C "format_print %{title}")
    artist=$(cmus-remote -C "format_print %{artist}")
    album=$(cmus-remote -C "format_print %{album}")
  elif [[ $current_source = "$ITUNES" ]]; then
    track=$(osascript -e 'try' -e 'tell application "iTunes" to name of current track as string' -e 'on error errText' -e '""' -e 'end try');
    artist=$(osascript -e 'try' -e 'tell application "iTunes" to artist of current track as string' -e 'on error errText' -e '""' -e 'end try');
    album=$(osascript -e 'try' -e 'tell application "iTunes" to album of current track as string' -e 'on error errText' -e '""' -e 'end try');
  elif [[ $current_source = "$MUSIC" ]]; then
    track=$(osascript -e 'try' -e 'tell application "Music" to name of current track as string' -e 'on error errText' -e '""' -e 'end try');
    artist=$(osascript -e 'try' -e 'tell application "Music" to artist of current track as string' -e 'on error errText' -e '""' -e 'end try');
    album=$(osascript -e 'try' -e 'tell application "Music" to album of current track as string' -e 'on error errText' -e '""' -e 'end try');
  elif [[ $current_source = "$PIANOBAR" ]]; then
    # First check if 'playing' file exists
    if [ -f "$pianobar_playingfile" ]; then
      IFS=$'\n' read -d '' -r -a lines < "$pianobar_playingfile"
      artist="${lines[0]}"
      track="${lines[1]}"
      album="${lines[2]}"
      station="${lines[3]}"
      rating="${lines[4]}"
    fi
  fi

  if [[ $track = "" || $artist = "" || $album = "" ]]; then
    echo "Nothing playing in $current_source"
    return 1
  else
    echo "Now playing in $current_source"
  fi

  # Get icon for current track, artist, album based on dark / light mode
  if [[ "$BitBarDarkMode" ]]; then
    track_icon=$note_icon_dark
    artist_icon=$person_icon_dark
    album_icon=$album_icon_dark
    station_icon=$station_icon_dark
    star_icon=$star_icon_dark
  else
    track_icon=$note_icon_light
    artist_icon=$person_icon_light
    album_icon=$album_icon_light
    station_icon=$station_icon_light
    star_icon=$star_icon_light
  fi

  echo "$track | image=$track_icon length=$display_length"
  echo "$artist | image=$artist_icon length=$display_length"
  echo "$album | image=$album_icon length=$display_length"

  if [[ $current_source = "$PIANOBAR" ]]; then
    echo "$station | image=$station_icon"

    # Experimental mode: TODO (sebbas): Cover art
    cover_url="${lines[5]}"
    if [[ $EXPERIMENTAL_MODE = 1 && $cover_url != "" ]]; then
      echo "---"
      cover_url="${lines[5]}"
      highres_pattern="500W_500H"
      lowres_pattern="130W_130H"
      thumb_url=${cover_url/$highres_pattern/$lowres_pattern}
      base64=$(curl -s "$thumb_url" | openssl base64 | tr -d '\n')
      echo " | image=$base64 length=$display_length trim=false"
    fi

    if [[ "$rating" = 1 ]]; then
      echo "Favorite Pandora song | image=$star_icon length=$display_length"
    fi
  fi
  return 0
}

function library_info
{
  if [[ $current_source = "$CMUS" ]]; then
    echo "My cmus library"

    exif=$(xxd -p "$cmus_cachefile" | tr -d '\n' | awk '{print $1"0"}' | perl -ne '$_.="0000";@exif=$_=~/(?<=f{112})(.*?)(?=0000)/g;print join"\n",@exif' | awk '{print "0066696c6500"$1}')

    # Experimental mode: TODO (sebbas): Album tag
    if [[ $EXPERIMENTAL_MODE = 1 ]]; then
      data=$(echo "$exif" | perl -ne '$_=~s/\n/00\n/g;@a=$_=~/(?<=0066696c6500)(.*?)(?=00)|(?<=0061727469737400)(.*?)(?=00)|(?<=00616c62756d00)(.*?)(?=00)|(?<=007469746c6500)(.*?)(?=00)/g; print "@a\n"; ')
      sorted=$(echo "$data" | sort -f -k 2)
      echo -e "$sorted" | perl -ne '$display_length=40; @a=split(/\s+/,$_); $a[0]=~s/\G..\K(?=.)/\\x/sg; $file="\\x".$a[0]; $artist=$a[1]; $album=$a[2]; $track=$a[3]; $file.="0" if(length($file) % 2 == 1); $artist.="0" if(length($artist) % 2 == 1); $album.="0" if(length($album) % 2 == 1); $track.="0" if(length($track) % 2 == 1); use Encode; binmode STDOUT, ":utf8"; $artist=Encode::decode("UTF-8", pack(q{H*}, $artist)); $album=Encode::decode("UTF-8", pack(q{H*}, $album)); $track=Encode::decode("UTF-8", pack(q{H*}, $track)); next if ($file eq "" || $artist eq "" || $album eq "" || $track eq ""); print "$artist | length=$display_length\n" if("$old_artist" ne "$artist"); print "--$album\n" if ("$old_album" ne "$album"); print "--$track | bash='"'$0'"' param1=\"cmus_song\" param2=\"$file\" terminal=false refresh=false length=$display_length\n"; $old_artist=$artist; $old_album=$album;'

    else
      data=$(echo "$exif" | perl -ne '$_=~s/\n/00\n/g;@a=$_=~/(?<=0066696c6500)(.*?)(?=00)|(?<=0061727469737400)(.*?)(?=00)|(?<=007469746c6500)(.*?)(?=00)/g; print "@a\n"; ')
      sorted=$(echo "$data" | sort -f -k 2)
      echo -e "$sorted" | perl -ne '$display_length=30; @a=split(/\s+/,$_); $a[0]=~s/\G..\K(?=.)/\\x/sg; $file="\\x".$a[0]; $artist=$a[1]; $track=$a[2]; $file.="0" if(length($file) % 2 == 1); $artist.="0" if(length($artist) % 2 == 1); $track.="0" if(length($track) % 2 == 1); use Encode; binmode STDOUT, ":utf8"; $artist=Encode::decode("UTF-8", pack(q{H*}, $artist)); $track=Encode::decode("UTF-8", pack(q{H*}, $track)); next if ($file eq "" || $artist eq "" || $track eq ""); print "$artist | length=$display_length\n" if("$oa" ne "$artist"); print "--$track | bash='"'$0'"' param1=\"cmus_song\" param2=\"$file\" terminal=false refresh=false length=$display_length\n"; $oa=$artist;'
    fi

  elif [[ $current_source = "$PIANOBAR" ]]; then
    echo "My Pandora stations"
    while read -r line; do

      # Split station number and name from each other, closing bracket is delimiter
      # shellcheck disable=SC2001
      station_num="$(sed 's/).*//' <<< "$line")"
      # shellcheck disable=SC2001
      station_name="$(sed 's/^[^)]*)//' <<< "$line")"

      # Remove leading and trailing white space
      station_num=$(echo "$station_num" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
      station_name=$(echo "$station_name" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')

      # Checked items are still beta, leaving this in anyways
      if [[ "$station_name" = "$station" ]]; then
        echo -e "$station_name | bash='$0' param1='pianobar_station' param2='$station_num' terminal=false refresh=false checked=true length=$display_length"
      else
        echo -e "$station_name | bash='$0' param1='pianobar_station' param2='$station_num' terminal=false refresh=false length=$display_length"
      fi
    done < "$pianobar_stationsfile"
  fi
}

# Set menu icon based on dark mode setup and display info sections
if [[ "$BitBarDarkMode" ]]; then
  echo "$track $artist $album | image=$list_icon_dark length=$display_length"
  echo "---"
else
  echo "$track $artist $album | image=$list_icon_light"
  echo "---"
fi

if playing_info; then
  echo "---"
  library_info
fi
