import React, { useState, useEffect } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import axios from "axios";
import { Button } from "./components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./components/ui/card";
import { Input } from "./components/ui/input";
import { Label } from "./components/ui/label";
import { Textarea } from "./components/ui/textarea";
import { Badge } from "./components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs";
import { Alert, AlertDescription } from "./components/ui/alert";
import { Separator } from "./components/ui/separator";
import { toast } from "sonner";
import { CheckCircle, Code, Github, Zap, Rocket, Coffee, Settings, ExternalLink } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Home = () => {
  const [languages, setLanguages] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [selectedLanguage, setSelectedLanguage] = useState(null);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [projectForm, setProjectForm] = useState({
    name: "",
    description: "",
    github_username: ""
  });
  const [recentProjects, setRecentProjects] = useState([]);

  useEffect(() => {
    fetchLanguages();
    fetchRecentProjects();
  }, []);

  const fetchLanguages = async () => {
    try {
      const response = await axios.get(`${API}/languages`);
      setLanguages(response.data.languages);
    } catch (error) {
      console.error("Error fetching languages:", error);
      toast.error("Failed to load languages");
    }
  };

  const fetchTemplates = async (languageId) => {
    try {
      const response = await axios.get(`${API}/templates/${languageId}`);
      setTemplates(response.data.templates);
    } catch (error) {
      console.error("Error fetching templates:", error);
      toast.error("Failed to load templates");
    }
  };

  const fetchRecentProjects = async () => {
    try {
      const response = await axios.get(`${API}/projects`);
      setRecentProjects(response.data.projects.slice(-3));
    } catch (error) {
      console.error("Error fetching projects:", error);
    }
  };

  const handleLanguageSelect = (language) => {
    setSelectedLanguage(language);
    setSelectedTemplate(null);
    fetchTemplates(language.id);
  };

  const handleTemplateSelect = (template) => {
    setSelectedTemplate(template);
  };

  const handleInputChange = (field, value) => {
    setProjectForm(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const generateProject = async () => {
    if (!selectedLanguage || !selectedTemplate) {
      toast.error("Please select a language and template");
      return;
    }

    if (!projectForm.name || !projectForm.github_username) {
      toast.error("Please fill in project name and GitHub username");
      return;
    }

    setIsGenerating(true);
    try {
      const response = await axios.post(`${API}/generate`, {
        name: projectForm.name,
        description: projectForm.description || `A ${selectedTemplate.name} project`,
        language: selectedLanguage.id,
        template_id: selectedTemplate.id,
        github_username: projectForm.github_username
      });

      if (response.data.success) {
        toast.success(
          <div className="flex flex-col gap-2">
            <span>{response.data.message}</span>
            <a 
              href={response.data.repository_url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-blue-500 hover:text-blue-700 flex items-center gap-1"
            >
              <ExternalLink className="w-4 h-4" />
              View Repository
            </a>
          </div>
        );
        
        // Reset form
        setProjectForm({ name: "", description: "", github_username: "" });
        setSelectedLanguage(null);
        setSelectedTemplate(null);
        setTemplates([]);
        
        // Refresh recent projects
        setTimeout(() => fetchRecentProjects(), 1000);
      }
    } catch (error) {
      const errorMessage = error.response?.data?.detail || "Failed to generate project";
      toast.error(errorMessage);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      {/* Header */}
      <header className="border-b border-white/20 backdrop-blur-lg bg-white/80 sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-xl flex items-center justify-center">
                <Code className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-700 to-indigo-700 bg-clip-text text-transparent">
                  Scaffold Forge
                </h1>
                <p className="text-sm text-slate-600">Template Generator System</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Github className="w-5 h-5 text-slate-600" />
              <span className="text-sm text-slate-600">Powered by GitHub</span>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-8">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 bg-blue-100 text-blue-800 px-4 py-2 rounded-full text-sm font-medium mb-6">
            <Zap className="w-4 h-4" />
            Similar to Santander Gluon
          </div>
          <h2 className="text-4xl font-bold text-slate-800 mb-4">
            Generate Projects in Seconds
          </h2>
          <p className="text-xl text-slate-600 max-w-2xl mx-auto">
            Create professional project scaffolds with GitHub integration. Choose from Java and .NET templates with CI/CD ready configurations.
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Main Generator */}
          <div className="lg:col-span-2">
            <Card className="shadow-xl border-0 bg-white/70 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Rocket className="w-5 h-5 text-blue-600" />
                  Project Generator
                </CardTitle>
                <CardDescription>
                  Create a new project repository with your chosen template
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Tabs defaultValue="language" className="w-full">
                  <TabsList className="grid w-full grid-cols-3">
                    <TabsTrigger value="language">1. Language</TabsTrigger>
                    <TabsTrigger value="template" disabled={!selectedLanguage}>2. Template</TabsTrigger>
                    <TabsTrigger value="details" disabled={!selectedTemplate}>3. Details</TabsTrigger>
                  </TabsList>

                  <TabsContent value="language" className="mt-6">
                    <div className="grid md:grid-cols-2 gap-4">
                      {languages.map((language) => (
                        <Card 
                          key={language.id}
                          className={`cursor-pointer transition-all hover:shadow-lg ${
                            selectedLanguage?.id === language.id 
                              ? 'ring-2 ring-blue-500 bg-blue-50' 
                              : 'hover:bg-slate-50'
                          }`}
                          onClick={() => handleLanguageSelect(language)}
                        >
                          <CardContent className="p-6">
                            <div className="flex items-center gap-3">
                              <span className="text-2xl">{language.icon}</span>
                              <div>
                                <h3 className="font-semibold text-lg">{language.name}</h3>
                                <p className="text-sm text-slate-600">{language.description}</p>
                              </div>
                            </div>
                            {selectedLanguage?.id === language.id && (
                              <CheckCircle className="w-5 h-5 text-blue-600 ml-auto" />
                            )}
                          </CardContent>
                        </Card>
                      ))}
                    </div>
                  </TabsContent>

                  <TabsContent value="template" className="mt-6">
                    <div className="grid md:grid-cols-2 gap-4">
                      {templates.map((template) => (
                        <Card 
                          key={template.id}
                          className={`cursor-pointer transition-all hover:shadow-lg ${
                            selectedTemplate?.id === template.id 
                              ? 'ring-2 ring-blue-500 bg-blue-50' 
                              : 'hover:bg-slate-50'
                          }`}
                          onClick={() => handleTemplateSelect(template)}
                        >
                          <CardContent className="p-6">
                            <div className="flex justify-between items-start mb-3">
                              <h3 className="font-semibold text-lg">{template.name}</h3>
                              <Badge variant="secondary">{template.type}</Badge>
                            </div>
                            <p className="text-sm text-slate-600 mb-3">{template.description}</p>
                            {selectedTemplate?.id === template.id && (
                              <CheckCircle className="w-5 h-5 text-blue-600" />
                            )}
                          </CardContent>
                        </Card>
                      ))}
                    </div>
                  </TabsContent>

                  <TabsContent value="details" className="mt-6">
                    <div className="space-y-6">
                      <div className="grid md:grid-cols-2 gap-4">
                        <div>
                          <Label htmlFor="project-name">Project Name *</Label>
                          <Input
                            id="project-name"
                            placeholder="my-awesome-project"
                            value={projectForm.name}
                            onChange={(e) => handleInputChange('name', e.target.value)}
                          />
                        </div>
                        <div>
                          <Label htmlFor="github-username">GitHub Username *</Label>
                          <Input
                            id="github-username"
                            placeholder="your-github-username"
                            value={projectForm.github_username}
                            onChange={(e) => handleInputChange('github_username', e.target.value)}
                          />
                        </div>
                      </div>
                      <div>
                        <Label htmlFor="description">Description</Label>
                        <Textarea
                          id="description"
                          placeholder="Brief description of your project..."
                          value={projectForm.description}
                          onChange={(e) => handleInputChange('description', e.target.value)}
                          rows={3}
                        />
                      </div>

                      {selectedLanguage && selectedTemplate && (
                        <Alert>
                          <Settings className="h-4 w-4" />
                          <AlertDescription>
                            Creating a <strong>{selectedTemplate.name}</strong> project in <strong>{selectedLanguage.name}</strong>
                            {projectForm.name && ` named "${projectForm.name}"`}
                          </AlertDescription>
                        </Alert>
                      )}

                      <Button 
                        onClick={generateProject}
                        disabled={isGenerating || !projectForm.name || !projectForm.github_username}
                        className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700"
                        size="lg"
                      >
                        {isGenerating ? (
                          <>
                            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                            Generating Project...
                          </>
                        ) : (
                          <>
                            <Rocket className="w-4 h-4 mr-2" />
                            Generate Project
                          </>
                        )}
                      </Button>
                    </div>
                  </TabsContent>
                </Tabs>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Recent Projects */}
            <Card className="shadow-lg border-0 bg-white/70 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-lg">
                  <Github className="w-5 h-5 text-slate-600" />
                  Recent Projects
                </CardTitle>
              </CardHeader>
              <CardContent>
                {recentProjects.length > 0 ? (
                  <div className="space-y-3">
                    {recentProjects.map((project, index) => (
                      <div key={index} className="p-3 bg-slate-50 rounded-lg">
                        <div className="flex justify-between items-start">
                          <div>
                            <h4 className="font-medium text-sm">{project.name}</h4>
                            <p className="text-xs text-slate-600">{project.language}</p>
                          </div>
                          <Badge variant="outline" className="text-xs">
                            {new Date(project.created_at).toLocaleDateString()}
                          </Badge>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-slate-500">No projects generated yet</p>
                )}
              </CardContent>
            </Card>

            {/* Features */}
            <Card className="shadow-lg border-0 bg-white/70 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="text-lg">Features</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex items-center gap-3">
                    <CheckCircle className="w-4 h-4 text-green-600" />
                    <span className="text-sm">GitHub Integration</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <CheckCircle className="w-4 h-4 text-green-600" />
                    <span className="text-sm">CI/CD Workflows</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <CheckCircle className="w-4 h-4 text-green-600" />
                    <span className="text-sm">Ready-to-use Templates</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <CheckCircle className="w-4 h-4 text-green-600" />
                    <span className="text-sm">Auto Project Setup</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;