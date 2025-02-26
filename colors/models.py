from django.db import models


class EmotionColor(models.Model):
    very_happy = models.CharField(max_length=7, default="#FFD700")  # Hex code
    very_relaxed = models.CharField(max_length=7, default="#FFFF00")
    relaxed = models.CharField(max_length=7, default="#FFFF00")
    neutral = models.CharField(max_length=7, default="#C0C0C0")
    sad = models.CharField(max_length=7, default="#87CEEB")
    very_sad = models.CharField(max_length=7, default="#1E90FF")
    is_breathing = models.BooleanField(default=False)

    very_happy_threshold = models.IntegerField(
        max_length=3, default=70
    )  # SDNN Threshold
    very_relaxed_threshold = models.IntegerField(max_length=3, default=60)
    relaxed_threshold = models.IntegerField(max_length=3, default=50)
    neutral_threshold = models.IntegerField(max_length=3, default=40)
    sad_threshold = models.IntegerField(max_length=3, default=30)
    very_sad_threshold = models.IntegerField(max_length=3, default=20)

    def to_dict(self):
        """
        Converts the model instance to a dictionary for easy JSON serialization.
        """
        return {
            "very_happy": self.very_happy,
            "very_relaxed": self.very_relaxed,
            "relaxed": self.relaxed,
            "neutral": self.neutral,
            "sad": self.sad,
            "very_sad": self.very_sad,
            "is_breathing": self.is_breathing,
            "very_happy_threshold": self.very_happy_threshold,
            "very_relaxed_threshold": self.very_relaxed_threshold,
            "relaxed_threshold": self.relaxed_threshold,
            "neutral_threshold": self.neutral_threshold,
            "sad_threshold": self.sad_threshold,
            "very_sad_threshold": self.very_sad_threshold,
        }
