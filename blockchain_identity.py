
import hashlib
import json
from datetime import datetime
from typing import Dict, List, Optional

class BlockchainIdentityVerification:
    def __init__(self):
        self.ledger: List[Dict] = []
        self.genesis_block()
        
    def genesis_block(self):
        """Create the first block in the chain"""
        self.ledger.append({
            "index": 0,
            "timestamp": datetime.now().isoformat(),
            "data": "Genesis Block",
            "previous_hash": "0",
            "hash": self.calculate_hash("0" + str(datetime.now().isoformat()) + "Genesis Block")
        })
        
    def calculate_hash(self, data: str) -> str:
        """Calculate SHA256 hash of input data"""
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
        
    def generate_identity_hash(self, user_data: Dict) -> str:
        """Generate a unique digital identity hash"""
        user_str = json.dumps(user_data, sort_keys=True)
        return hashlib.sha256(user_str.encode('utf-8')).hexdigest()
        
    def create_verification_record(self, user_id: str, user_name: str, identity_data: Dict) -> Dict:
        """Create a new verification record and add to the ledger"""
        last_block = self.ledger[-1]
        index = last_block["index"] + 1
        identity_hash = self.generate_identity_hash({
            "user_id": user_id,
            "user_name": user_name,
            "identity_data": identity_data,
            "timestamp": datetime.now().isoformat()
        })
        
        verification_record = {
            "index": index,
            "timestamp": datetime.now().isoformat(),
            "data": {
                "user_id": user_id,
                "user_name": user_name,
                "identity_data": identity_data,
                "status": "Verified",
                "trust_score": 98
            },
            "previous_hash": last_block["hash"],
            "hash": None
        }
        
        verification_record["hash"] = self.calculate_hash(
            str(index) + verification_record["timestamp"] + json.dumps(verification_record["data"]) + last_block["hash"])
        
        self.ledger.append(verification_record)
        
        return {
            "success": True,
            "user_id": user_id,
            "verification_status": "Verified",
            "blockchain_transaction_id": verification_record["hash"],
            "digital_identity_hash": identity_hash,
            "verification_date": datetime.now().strftime("%d-%m-%Y"),
            "trust_score": 98,
            "blockchain_status": "Successfully Recorded",
            "final_result": "Authentic Verified Identity"
        }
        
    def verify_identity(self, username: str, bio: str, has_profile_picture: int) -> Dict:
        """Verify identity using blockchain"""
        user_data = {
            "username": username,
            "bio": bio,
            "has_profile_picture": has_profile_picture
        }
        
        trust_score = 20
        
        if has_profile_picture:
            trust_score += 30
            
        if len(bio) > 50:
            trust_score += 30
            
        if len(bio) > 100:
            trust_score += 20
            
        verification_status = "Not Verified"
        if trust_score >= 80:
            verification_status = "Verified"
            final_result = "Authentic Verified Identity"
        else:
            final_result = "No Identity Verification Found"
            
        digital_identity_hash = self.generate_identity_hash(user_data)
        
        return {
            "username": username,
            "verification_status": verification_status,
            "trust_score": trust_score,
            "digital_identity_hash": digital_identity_hash,
            "verification_badge": verification_status == "Verified",
            "final_result": final_result
        }
        
    def get_verification_history(self) -> List[Dict]:
        """Get all verification records"""
        history = []
        for block in self.ledger:
            if "user_id" in block.get("data", {}):
                history.append({
                    "user_id": block["data"]["user_id"],
                    "user_name": block["data"]["user_name"],
                    "status": block["data"]["status"],
                    "trust_score": block["data"]["trust_score"],
                    "transaction_id": block["hash"],
                    "date": datetime.fromisoformat(block["timestamp"]).strftime("%d-%m-%Y %H:%M:%S")
                })
        return history
        
    def generate_sample_verifications(self, count: int = 5) -> List[Dict]:
        """Generate sample verification data for demonstration"""
        sample_users = [
            {"user_id": "USR1001", "user_name": "Alice Smith", "country": "USA"},
            {"user_id": "USR1002", "user_name": "Bob Johnson", "country": "UK"},
            {"user_id": "USR1003", "user_name": "Charlie Brown", "country": "Canada"},
            {"user_id": "USR1004", "user_name": "Diana Prince", "country": "Germany"},
            {"user_id": "USR1005", "user_name": "Ethan Hunt", "country": "Australia"}
        ]
        
        for user in sample_users:
            self.create_verification_record(user["user_id"], user["user_name"], user)
        
        return self.get_verification_history()

identity_system = BlockchainIdentityVerification()

