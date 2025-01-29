from django.db import models

class EmotionColor(models.Model):
    very_happy = models.CharField(max_length=7, default="#FFD700")  # Hex code
    happy = models.CharField(max_length=7, default="#FFFF00")
    neutral = models.CharField(max_length=7, default="#C0C0C0")
    sad = models.CharField(max_length=7, default="#87CEEB")
    very_sad = models.CharField(max_length=7, default="#1E90FF")

    def to_dict(self):
        """
        Converts the model instance to a dictionary for easy JSON serialization.
        """
        return {
            "very_happy": self.very_happy,
            "happy": self.happy,
            "neutral": self.neutral,
            "sad": self.sad,
            "very_sad": self.very_sad,
        }
