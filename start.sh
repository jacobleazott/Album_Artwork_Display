DISPLAY=:0 xrandr --output HDMI-1 --rotate right
cd ~/projects/Spotify_Release_Pi/
source .venv/bin/activate
source tokens/spotify_token.sh
cd ~/projects/Album_Artwork_Display/
python Gather_Album_Artwork.py