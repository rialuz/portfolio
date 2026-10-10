// Written by tools/seasons.py: the same data as public/sprites/seasons/manifest.json.
window.SEASONS = {
  "default": "candy",
  "replaces": [
    "bg-hero",
    "bg-cloud-1",
    "bg-cloud-2",
    "bg-cloud-3",
    "prop-cloud",
    "prop-flag",
    "tile-road-straight",
    "tile-road-corner",
    "tile-road-faded"
  ],
  "interface": [
    "ui-dialogue-frame",
    "ui-nameplate"
  ],
  "character": [
    "luz-base-front",
    "luz-side-right",
    "luz-idle",
    "luz-wave",
    "luz-walk",
    "luz-walk-down",
    "luz-walk-up",
    "luz-hop",
    "luz-emote-wow",
    "luz-emote-grin",
    "luz-emote-happy",
    "luz-emote-starry",
    "luz-emote-student",
    "luz-emote-cheer",
    "luz-portrait"
  ],
  "seasons": {
    "halloween": {
      "label": "Halloween",
      "sky": "#3b2861",
      "ground": "#231a3a",
      "plate": "#3d3058",
      "foreground": true,
      "clouds": [
        {
          "sheet": "bg-cloud-1",
          "x": 33,
          "y": 22
        },
        {
          "sheet": "bg-cloud-2",
          "x": 150,
          "y": 34
        },
        {
          "sheet": "bg-cloud-3",
          "x": 81,
          "y": 56
        }
      ],
      "sprites": {
        "prop-pumpkin": {
          "w": 32,
          "h": 32,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "prop-tombstone": {
          "w": 32,
          "h": 32,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "prop-cauldron": {
          "w": 32,
          "h": 32,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "prop-witch-hat": {
          "w": 32,
          "h": 32,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "prop-black-cat": {
          "w": 32,
          "h": 32,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "fx-bat": {
          "w": 32,
          "h": 32,
          "frames": 4,
          "duration": 0.5,
          "loop": true
        },
        "fx-ghost": {
          "w": 32,
          "h": 32,
          "frames": 4,
          "duration": 1.4,
          "loop": true
        },
        "fx-pumpkin": {
          "w": 32,
          "h": 32,
          "frames": 4,
          "duration": 0.9,
          "loop": true
        }
      },
      "ambient": [
        {
          "sheet": "fx-bat",
          "x": 232,
          "y": 30,
          "scale": "character",
          "layer": "back",
          "motion": "drift",
          "to": "left",
          "seconds": 26
        },
        {
          "sheet": "fx-bat",
          "x": 128,
          "y": 58,
          "low": {
            "x": -60
          },
          "scale": "character",
          "layer": "back",
          "motion": "drift",
          "to": "right",
          "seconds": 34
        },
        {
          "sheet": "fx-bat",
          "x": 176,
          "y": 12,
          "scale": "character",
          "layer": "back",
          "motion": "drift",
          "to": "left",
          "seconds": 44
        },
        {
          "sheet": "fx-ghost",
          "x": 204,
          "y": 126,
          "scale": "character",
          "layer": "front",
          "motion": "still"
        },
        {
          "sheet": "fx-pumpkin",
          "x": 206,
          "y": 149,
          "scale": "character",
          "layer": "front",
          "motion": "still"
        }
      ],
      "roadWalkers": [
        "fx-ghost"
      ]
    },
    "valentines": {
      "label": "Valentine's Day",
      "sky": "#f9b2cf",
      "ground": "#4d323a",
      "plate": "#a32239",
      "foreground": false,
      "clouds": [
        {
          "sheet": "bg-cloud-1",
          "x": 33,
          "y": 22
        },
        {
          "sheet": "bg-cloud-2",
          "x": 262,
          "y": 20
        },
        {
          "sheet": "bg-cloud-3",
          "x": 118,
          "y": 28
        }
      ],
      "sprites": {
        "prop-teddy": {
          "w": 32,
          "h": 32,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "prop-gift": {
          "w": 32,
          "h": 32,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "prop-rose": {
          "w": 32,
          "h": 32,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "prop-heart-lock": {
          "w": 32,
          "h": 32,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "prop-chocolates": {
          "w": 32,
          "h": 32,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "prop-love-letter": {
          "w": 32,
          "h": 32,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "fx-heart": {
          "w": 16,
          "h": 16,
          "frames": 4,
          "duration": 0.9,
          "loop": true
        },
        "fx-heart-arrow": {
          "w": 24,
          "h": 9,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "fx-cupid": {
          "w": 96,
          "h": 84,
          "frames": 12,
          "duration": 2.4,
          "loop": true
        }
      },
      "ambient": [
        {
          "sheet": "fx-cupid",
          "x": 196,
          "y": 26,
          "low": {
            "x": 100
          },
          "scale": "character",
          "layer": "back",
          "motion": "drift",
          "to": "right",
          "seconds": 38
        },
        {
          "sheet": "fx-heart",
          "x": 104,
          "y": 82,
          "scale": "character",
          "layer": "back",
          "motion": "hover"
        },
        {
          "sheet": "fx-heart",
          "x": 262,
          "y": 104,
          "scale": "character",
          "layer": "back",
          "motion": "hover",
          "delay": -0.4
        }
      ],
      "roadWalkers": [
        "fx-heart"
      ]
    },
    "easter": {
      "label": "Easter",
      "sky": "#9ff8fa",
      "ground": "#a9764a",
      "plate": "#6247a3",
      "foreground": false,
      "clouds": [
        {
          "sheet": "bg-cloud-1",
          "x": 24,
          "y": 30
        },
        {
          "sheet": "bg-cloud-2",
          "x": 118,
          "y": 6
        },
        {
          "sheet": "bg-cloud-3",
          "x": 175,
          "y": 24
        }
      ],
      "sprites": {
        "prop-basket": {
          "w": 32,
          "h": 32,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "prop-tulip": {
          "w": 32,
          "h": 32,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "prop-daffodil": {
          "w": 32,
          "h": 32,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "prop-chick": {
          "w": 32,
          "h": 32,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "prop-carrot": {
          "w": 32,
          "h": 32,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "prop-butterfly": {
          "w": 32,
          "h": 32,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "prop-egg-pink": {
          "w": 32,
          "h": 32,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "prop-egg-blue": {
          "w": 32,
          "h": 32,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "prop-egg-yellow": {
          "w": 32,
          "h": 32,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "prop-egg-lilac": {
          "w": 32,
          "h": 32,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "fx-bunny": {
          "w": 48,
          "h": 32,
          "frames": 6,
          "duration": 0.72,
          "loop": true
        },
        "fx-butterfly": {
          "w": 16,
          "h": 16,
          "frames": 4,
          "duration": 0.5,
          "loop": true
        }
      },
      "ambient": [
        {
          "sheet": "fx-bunny",
          "x": -40,
          "y": 149,
          "x2": 344,
          "rest": 108,
          "scale": "character",
          "layer": "front",
          "motion": "stride",
          "stride": 16
        },
        {
          "sheet": "fx-butterfly",
          "x": 34,
          "y": 126,
          "scale": "character",
          "layer": "front",
          "motion": "hover"
        },
        {
          "sheet": "fx-butterfly",
          "x": 300,
          "y": 118,
          "scale": "character",
          "layer": "front",
          "motion": "hover",
          "delay": -1.3
        }
      ],
      "roadWalkers": [
        "fx-butterfly"
      ]
    },
    "summer": {
      "label": "Summer",
      "sky": "#65f2f4",
      "ground": "#d9ad74",
      "plate": "#136f7a",
      "foreground": true,
      "clouds": [
        {
          "sheet": "bg-cloud-1",
          "x": 33,
          "y": 22
        },
        {
          "sheet": "bg-cloud-2",
          "x": 221,
          "y": 25
        },
        {
          "sheet": "bg-cloud-3",
          "x": 81,
          "y": 53
        }
      ],
      "sprites": {
        "prop-palm": {
          "w": 48,
          "h": 64,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "prop-umbrella": {
          "w": 48,
          "h": 48,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "prop-lawn-chair": {
          "w": 32,
          "h": 32,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "prop-shell": {
          "w": 32,
          "h": 32,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "prop-starfish": {
          "w": 32,
          "h": 32,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "prop-life-ring": {
          "w": 32,
          "h": 32,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "prop-watermelon": {
          "w": 32,
          "h": 32,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "prop-drink": {
          "w": 32,
          "h": 32,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "prop-dolphin": {
          "w": 48,
          "h": 32,
          "frames": 1,
          "duration": 0,
          "loop": false
        },
        "fx-wave": {
          "w": 344,
          "h": 50,
          "frames": 4,
          "duration": 2.4,
          "loop": true
        },
        "fx-dolphin": {
          "w": 48,
          "h": 28,
          "frames": 16,
          "duration": 3.2,
          "loop": true
        },
        "fx-crab": {
          "w": 32,
          "h": 32,
          "frames": 4,
          "duration": 0.5,
          "loop": true
        }
      },
      "ambient": [
        {
          "sheet": "fx-wave",
          "x": 0,
          "y": 124,
          "scale": "bg",
          "layer": "back",
          "motion": "still"
        },
        {
          "sheet": "fx-dolphin",
          "x": 118,
          "y": 108,
          "scale": "bg",
          "layer": "back",
          "motion": "still"
        },
        {
          "sheet": "fx-dolphin",
          "x": 196,
          "y": 110,
          "scale": "bg",
          "layer": "back",
          "motion": "still",
          "delay": -1.6,
          "flipped": true
        },
        {
          "sheet": "fx-crab",
          "x": 96,
          "y": 149,
          "x2": 150,
          "scale": "character",
          "layer": "front",
          "motion": "patrol"
        }
      ],
      "roadWalkers": [
        "fx-crab"
      ]
    }
  }
};
