import requests
import sys
import json
from datetime import datetime

class ScaffoldForgeAPITester:
    def __init__(self, base_url="https://scaffold-forge.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}" if endpoint else f"{self.api_url}"
        if headers is None:
            headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)

            print(f"   Status Code: {response.status_code}")
            
            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
                    return True, response_data
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error: {response.text}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_root_endpoint(self):
        """Test root API endpoint"""
        return self.run_test("Root API Endpoint", "GET", "", 200)

    def test_get_languages(self):
        """Test languages endpoint"""
        success, response = self.run_test("Get Languages", "GET", "languages", 200)
        if success:
            languages = response.get('languages', [])
            if len(languages) >= 2:
                java_found = any(lang['id'] == 'java' for lang in languages)
                dotnet_found = any(lang['id'] == 'dotnet' for lang in languages)
                if java_found and dotnet_found:
                    print("   ✅ Found both Java and .NET languages")
                    return True, response
                else:
                    print("   ❌ Missing expected languages")
            else:
                print("   ❌ Expected at least 2 languages")
        return success, response

    def test_get_java_templates(self):
        """Test Java templates endpoint"""
        success, response = self.run_test("Get Java Templates", "GET", "templates/java", 200)
        if success:
            templates = response.get('templates', [])
            if len(templates) >= 2:
                hello_found = any(t['id'] == 'java-hello' for t in templates)
                spring_found = any(t['id'] == 'java-springboot' for t in templates)
                if hello_found and spring_found:
                    print("   ✅ Found both Java Hello World and Spring Boot templates")
                    return True, response
                else:
                    print("   ❌ Missing expected Java templates")
            else:
                print("   ❌ Expected at least 2 Java templates")
        return success, response

    def test_get_dotnet_templates(self):
        """Test .NET templates endpoint"""
        success, response = self.run_test("Get .NET Templates", "GET", "templates/dotnet", 200)
        if success:
            templates = response.get('templates', [])
            if len(templates) >= 2:
                console_found = any(t['id'] == 'dotnet-console' for t in templates)
                webapi_found = any(t['id'] == 'dotnet-webapi' for t in templates)
                if console_found and webapi_found:
                    print("   ✅ Found both .NET Console and Web API templates")
                    return True, response
                else:
                    print("   ❌ Missing expected .NET templates")
            else:
                print("   ❌ Expected at least 2 .NET templates")
        return success, response

    def test_get_invalid_templates(self):
        """Test invalid language templates endpoint"""
        return self.run_test("Get Invalid Templates", "GET", "templates/invalid", 404)

    def test_get_projects(self):
        """Test projects endpoint"""
        return self.run_test("Get Projects", "GET", "projects", 200)

    def test_generate_java_project(self):
        """Test Java project generation"""
        project_data = {
            "name": f"test-java-project-{datetime.now().strftime('%H%M%S')}",
            "description": "Test Java Hello World project generated by automated testing",
            "language": "java",
            "template_id": "java-hello",
            "github_username": "test-user-123"
        }
        
        success, response = self.run_test(
            "Generate Java Project", 
            "POST", 
            "generate", 
            200, 
            data=project_data
        )
        
        if success:
            if response.get('success') and response.get('repository_url'):
                print(f"   ✅ Project created successfully: {response.get('repository_url')}")
                return True, response
            else:
                print("   ❌ Project generation response missing success or repository_url")
        return success, response

    def test_generate_dotnet_project(self):
        """Test .NET project generation"""
        project_data = {
            "name": f"test-dotnet-project-{datetime.now().strftime('%H%M%S')}",
            "description": "Test .NET Console project generated by automated testing",
            "language": "dotnet",
            "template_id": "dotnet-console",
            "github_username": "test-user-123"
        }
        
        success, response = self.run_test(
            "Generate .NET Project", 
            "POST", 
            "generate", 
            200, 
            data=project_data
        )
        
        if success:
            if response.get('success') and response.get('repository_url'):
                print(f"   ✅ Project created successfully: {response.get('repository_url')}")
                return True, response
            else:
                print("   ❌ Project generation response missing success or repository_url")
        return success, response

    def test_generate_invalid_project(self):
        """Test project generation with invalid data"""
        project_data = {
            "name": "test-project",
            "description": "Test project",
            "language": "invalid",
            "template_id": "invalid",
            "github_username": "test-user-123"
        }
        
        return self.run_test(
            "Generate Invalid Project", 
            "POST", 
            "generate", 
            400, 
            data=project_data
        )

    def test_generate_missing_fields(self):
        """Test project generation with missing required fields"""
        project_data = {
            "name": "test-project"
            # Missing required fields
        }
        
        return self.run_test(
            "Generate Project Missing Fields", 
            "POST", 
            "generate", 
            422, 
            data=project_data
        )

def main():
    print("🚀 Starting Scaffold Forge API Testing...")
    print("=" * 60)
    
    tester = ScaffoldForgeAPITester()
    
    # Test all endpoints
    test_results = []
    
    # Basic endpoint tests
    test_results.append(tester.test_root_endpoint())
    test_results.append(tester.test_get_languages())
    test_results.append(tester.test_get_java_templates())
    test_results.append(tester.test_get_dotnet_templates())
    test_results.append(tester.test_get_invalid_templates())
    test_results.append(tester.test_get_projects())
    
    # Project generation tests
    test_results.append(tester.test_generate_java_project())
    test_results.append(tester.test_generate_dotnet_project())
    test_results.append(tester.test_generate_invalid_project())
    test_results.append(tester.test_generate_missing_fields())
    
    # Print final results
    print("\n" + "=" * 60)
    print(f"📊 FINAL RESULTS: {tester.tests_passed}/{tester.tests_run} tests passed")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed!")
        return 0
    else:
        print(f"❌ {tester.tests_run - tester.tests_passed} tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())