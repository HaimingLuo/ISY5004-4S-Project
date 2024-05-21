import math

class GestureRecognition:
    def classify_gesture(self, landmarks):
        # Calculate scores for each gesture
        tiger_score = self.calculate_tiger_score(landmarks)
        gun_score = self.calculate_gun_score(landmarks)
        heart_score = self.calculate_heart_score(landmarks)
        love_u_score = self.calculate_love_u_score(landmarks)
        bad_score = self.calculate_bad_score(landmarks)

        # Create a dictionary of gestures and their scores
        scores = {
            "Tiger": tiger_score,
            "Gun": gun_score,
            "Heart": heart_score,
            "Love U": love_u_score,
            "Bad": bad_score
        }

        # Find the gesture with the highest score
        best_gesture = max(scores, key=scores.get)
        return best_gesture, scores[best_gesture]

    def calculate_distance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

    def calculate_angle(self, point1, point2, point3):
        a = self.calculate_distance(point2, point3)
        b = self.calculate_distance(point1, point3)
        c = self.calculate_distance(point1, point2)
        if a * b == 0:
            return 0
        return math.degrees(math.acos((a**2 + b**2 - c**2) / (2 * a * b)))

    def calculate_tiger_score(self, landmarks):
        # Implement Tiger gesture score calculation logic
        # Example: Check if the fingers are spread wide apart
        distances = [
            self.calculate_distance(landmarks[4], landmarks[8]),  # Thumb to index
            self.calculate_distance(landmarks[8], landmarks[12]),  # Index to middle
            self.calculate_distance(landmarks[12], landmarks[16]),  # Middle to ring
            self.calculate_distance(landmarks[16], landmarks[20])  # Ring to pinky
        ]
        score = sum(distances)
        return score

    def calculate_gun_score(self, landmarks):
        # Implement Gun gesture score calculation logic
        # Example: Check if index and thumb form a gun shape
        thumb_index_distance = self.calculate_distance(landmarks[4], landmarks[8])
        thumb_pinky_distance = self.calculate_distance(landmarks[4], landmarks[20])
        index_middle_distance = self.calculate_distance(landmarks[8], landmarks[12])
        score = thumb_index_distance + (1 / thumb_pinky_distance if thumb_pinky_distance != 0 else 0) - index_middle_distance
        return score

    def calculate_heart_score(self, landmarks):
        # Implement Heart gesture score calculation logic
        # Example: Check if thumbs and index fingers form a heart shape
        left_angle = self.calculate_angle(landmarks[4], landmarks[8], landmarks[12])
        right_angle = self.calculate_angle(landmarks[4], landmarks[20], landmarks[16])
        score = abs(left_angle - 60) + abs(right_angle - 60)
        return score

    def calculate_love_u_score(self, landmarks):
        # Implement Love U gesture score calculation logic
        # Example: Check if the hand forms the "I love you" sign
        thumb_index_angle = self.calculate_angle(landmarks[4], landmarks[8], landmarks[6])
        index_middle_angle = self.calculate_angle(landmarks[8], landmarks[12], landmarks[10])
        middle_ring_angle = self.calculate_angle(landmarks[12], landmarks[16], landmarks[14])
        ring_pinky_angle = self.calculate_angle(landmarks[16], landmarks[20], landmarks[18])
        score = thumb_index_angle + index_middle_angle - middle_ring_angle - ring_pinky_angle
        return score

    def calculate_bad_score(self, landmarks):
        # Implement Bad gesture score calculation logic
        # Example: Check if thumb is pointing down and other fingers are curled
        thumb_angle = self.calculate_angle(landmarks[2], landmarks[3], landmarks[4])
        finger_angles = [
            self.calculate_angle(landmarks[6], landmarks[7], landmarks[8]),
            self.calculate_angle(landmarks[10], landmarks[11], landmarks[12]),
            self.calculate_angle(landmarks[14], landmarks[15], landmarks[16]),
            self.calculate_angle(landmarks[18], landmarks[19], landmarks[20])
        ]
        score = (180 - thumb_angle) + sum(finger_angles)
        return score
