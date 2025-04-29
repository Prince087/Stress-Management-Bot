import os
import google.generativeai as genai
from datetime import datetime
import json
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

SECRET_KEY = os.getenv("SECRET_KEY")

class StressBot:
    def __init__(self):
        # Initialize the Gemini model
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        self.user_profile = {}
        self.conversation_history = []
        self.stress_info = {
            "stress_level": None,
            "stress_triggers": [],
            "coping_mechanisms": [],
            "sleep_quality": None,
            "physical_symptoms": [],
            "emotional_symptoms": []
        }
    
    def save_profile(self, filename="user_profile.json"):
        """Save the user profile to a file"""
        with open(filename, 'w') as f:
            json.dump({"profile": self.user_profile, "stress_info": self.stress_info}, f)
        return "User profile saved successfully!"
    
    def load_profile(self, filename="user_profile.json"):
        """Load the user profile from a file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.user_profile = data.get("profile", {})
                self.stress_info = data.get("stress_info", {})
            return "User profile loaded successfully!"
        except FileNotFoundError:
            return "No profile found. Let's create a new one!"
    
    def update_profile(self, name=None, age=None, occupation=None):
        """Update the user profile with basic information"""
        if name:
            self.user_profile["name"] = name
        if age:
            self.user_profile["age"] = age
        if occupation:
            self.user_profile["occupation"] = occupation
        return "Profile updated successfully!"
    
    def set_stress_info(self, stress_level=None, triggers=None, coping_mechanisms=None, 
                       sleep_quality=None, physical_symptoms=None, emotional_symptoms=None):
        """Update the stress information"""
        if stress_level:
            self.stress_info["stress_level"] = stress_level
        if triggers:
            self.stress_info["stress_triggers"] = triggers if isinstance(triggers, list) else [triggers]
        if coping_mechanisms:
            self.stress_info["coping_mechanisms"] = coping_mechanisms if isinstance(coping_mechanisms, list) else [coping_mechanisms]
        if sleep_quality:
            self.stress_info["sleep_quality"] = sleep_quality
        if physical_symptoms:
            self.stress_info["physical_symptoms"] = physical_symptoms if isinstance(physical_symptoms, list) else [physical_symptoms]
        if emotional_symptoms:
            self.stress_info["emotional_symptoms"] = emotional_symptoms if isinstance(emotional_symptoms, list) else [emotional_symptoms]
        return "Stress information updated successfully!"
    
    def assess_stress_level(self):
        """Assess the user's stress level based on current information"""
        prompt = f"""
        Assess the stress level of a person with the following information:
        
        Stress triggers: {', '.join(self.stress_info['stress_triggers']) if self.stress_info['stress_triggers'] else 'None specified'}
        Physical symptoms: {', '.join(self.stress_info['physical_symptoms']) if self.stress_info['physical_symptoms'] else 'None specified'}
        Emotional symptoms: {', '.join(self.stress_info['emotional_symptoms']) if self.stress_info['emotional_symptoms'] else 'None specified'}
        Sleep quality: {self.stress_info['sleep_quality'] or 'Not specified'}
        
        Provide:
        1. An assessment of their current stress level (low, moderate, high, or severe)
        2. Potential health risks associated with their current stress level
        3. Recommendations for stress reduction
        4. Signs that indicate they should seek professional help
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def suggest_coping_strategies(self):
        """Suggest coping strategies based on the user's situation"""
        prompt = f"""
        Suggest personalized stress management strategies based on:
        Stress level: {self.stress_info['stress_level'] or 'Not specified'}
        Stress triggers: {', '.join(self.stress_info['stress_triggers']) if self.stress_info['stress_triggers'] else 'None specified'}
        Current coping mechanisms: {', '.join(self.stress_info['coping_mechanisms']) if self.stress_info['coping_mechanisms'] else 'None specified'}
        
        Include:
        1. Immediate stress relief techniques
        2. Long-term stress management strategies
        3. Mindfulness and meditation exercises
        4. Physical activity recommendations
        5. Sleep improvement tips
        6. Time management strategies
        7. Boundary-setting techniques
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def provide_relaxation_exercises(self):
        """Provide relaxation exercises based on the user's profile"""
        prompt = f"""
        Provide relaxation exercises based on:
        Stress level: {self.stress_info['stress_level'] or 'Not specified'}
        Physical symptoms: {', '.join(self.stress_info['physical_symptoms']) if self.stress_info['physical_symptoms'] else 'None specified'}
        Emotional symptoms: {', '.join(self.stress_info['emotional_symptoms']) if self.stress_info['emotional_symptoms'] else 'None specified'}
        
        Include:
        1. Breathing exercises with step-by-step instructions
        2. Progressive muscle relaxation techniques
        3. Guided imagery exercises
        4. Mindfulness meditation scripts
        5. Body scan exercises
        6. Quick relaxation techniques for busy situations
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def suggest_lifestyle_changes(self):
        """Provide lifestyle change recommendations"""
        prompt = f"""
        Suggest lifestyle changes to reduce stress based on:
        Stress level: {self.stress_info['stress_level'] or 'Not specified'}
        Sleep quality: {self.stress_info['sleep_quality'] or 'Not specified'}
        Stress triggers: {', '.join(self.stress_info['stress_triggers']) if self.stress_info['stress_triggers'] else 'None specified'}
        
        Include:
        1. Sleep hygiene recommendations
        2. Dietary changes to support stress reduction
        3. Exercise recommendations
        4. Social connection strategies
        5. Work-life balance techniques
        6. Time management tips
        7. Digital wellness practices
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def process_message(self, user_message):
        """Process user messages and generate appropriate responses"""
        # Add message to conversation history
        self.conversation_history.append({"role": "user", "content": user_message})
        
        # Extract information from user message
        if "stress level" in user_message.lower():
            level_match = re.search(r"(low|moderate|high|severe)", user_message.lower())
            if level_match:
                self.stress_info["stress_level"] = level_match.group(1)
        
        # Generate response based on message content
        if "stress level" in user_message.lower() or "assess" in user_message.lower():
            response = self.assess_stress_level()
        elif "coping" in user_message.lower() or "strategies" in user_message.lower():
            response = self.suggest_coping_strategies()
        elif "relax" in user_message.lower() or "exercise" in user_message.lower():
            response = self.provide_relaxation_exercises()
        elif "lifestyle" in user_message.lower() or "change" in user_message.lower():
            response = self.suggest_lifestyle_changes()
        else:
            # Default response for general queries
            prompt = f"""
            You are a helpful stress management assistant. The user has provided the following information:
            Stress level: {self.stress_info['stress_level'] or 'Not specified'}
            Stress triggers: {', '.join(self.stress_info['stress_triggers']) if self.stress_info['stress_triggers'] else 'None specified'}
            Physical symptoms: {', '.join(self.stress_info['physical_symptoms']) if self.stress_info['physical_symptoms'] else 'None specified'}
            Emotional symptoms: {', '.join(self.stress_info['emotional_symptoms']) if self.stress_info['emotional_symptoms'] else 'None specified'}
            
            Please provide a helpful response to: {user_message}
            
            Focus on:
            1. Stress assessment
            2. Coping strategies
            3. Relaxation techniques
            4. Lifestyle changes
            5. When to seek professional help
            """
            
            response = self.model.generate_content(prompt)
            response = response.text
        
        # Add response to conversation history
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response

def main():
    bot = StressBot()
    print("Stress Management Assistant initialized. Type 'quit' to exit.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        
        response = bot.process_message(user_input)
        print("Assistant:", response)

if __name__ == "__main__":
    main()