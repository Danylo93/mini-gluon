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
import { Progress } from "./components/ui/progress";
import { Skeleton } from "./components/ui/skeleton";
import { Switch } from "./components/ui/switch";
import { toast } from "sonner";
import useTheme from "./hooks/useTheme";
import LoadingSpinner from "./components/LoadingSpinner";
import StatsCard from "./components/StatsCard";
import { 
  CheckCircle, 
  Code, 
  Github, 
  Zap, 
  Rocket, 
  Coffee, 
  Settings, 
  ExternalLink, 
  Moon, 
  Sun, 
  Loader2,
  Star,
  TrendingUp,
  Users,
  Clock,
  ArrowRight,
  Copy,
  Download,
  Eye,
  Heart
} from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';
const API = `${BACKEND_URL}/api`;

const Home = () => {
  const { isDarkMode, toggleTheme } = useTheme();
  const [languages, setLanguages] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [selectedLanguage, setSelectedLanguage] = useState(null);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [projectForm, setProjectForm] = useState({
    name: "",
    description: "",
    github_username: ""
  });
  const [recentProjects, setRecentProjects] = useState([]);
  const [stats, setStats] = useState({
    totalProjects: 0,
    totalTemplates: 0,
    totalLanguages: 0
  });

  useEffect(() => {
    fetchLanguages();
    fetchRecentProjects();
    fetchStats();
    
    // Simular progresso de carregamento
    const progressInterval = setInterval(() => {
      setLoadingProgress(prev => {
        if (prev >= 100) {
          clearInterval(progressInterval);
          return 100;
        }
        return prev + 10;
      });
    }, 200);

    return () => clearInterval(progressInterval);
  }, []);


  const fetchLanguages = async () => {
    try {
      console.log("Fetching languages from:", `${API}/templates/languages`);
      const response = await axios.get(`${API}/templates/languages`);
      console.log("Languages response:", response.data);
      setLanguages(response.data?.languages || []);
    } catch (error) {
      console.error("Error fetching languages:", error);
      console.error("Error details:", error.response?.data);
      toast.error("Failed to load languages");
      setLanguages([]);
    }
  };

  const fetchTemplates = async (languageId) => {
    try {
      const response = await axios.get(`${API}/templates/${languageId}`);
      setTemplates(response.data?.templates || []);
    } catch (error) {
      console.error("Error fetching templates:", error);
      toast.error("Failed to load templates");
      setTemplates([]);
    }
  };

  const fetchRecentProjects = async () => {
    try {
      const response = await axios.get(`${API}/projects`);
      const projects = response.data?.projects || [];
      setRecentProjects(projects.slice(-3));
    } catch (error) {
      console.error("Error fetching projects:", error);
      setRecentProjects([]);
    }
  };

  const fetchStats = async () => {
    try {
      // Simular estatísticas (em um app real, isso viria da API)
      setStats({
        totalProjects: 1247,
        totalTemplates: 15,
        totalLanguages: 2
      });
    } catch (error) {
      console.error("Error fetching stats:", error);
    }
  };

  const copyToClipboard = async (text) => {
    try {
      await navigator.clipboard.writeText(text);
      toast.success("Copied to clipboard!");
    } catch (error) {
      toast.error("Failed to copy to clipboard");
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
    setLoadingProgress(0);
    
    // Simular progresso durante a geração
    const progressInterval = setInterval(() => {
      setLoadingProgress(prev => {
        if (prev >= 90) {
          clearInterval(progressInterval);
          return 90;
        }
        return prev + 15;
      });
    }, 500);

    try {
      const response = await axios.post(`${API}/projects/`, {
        name: projectForm.name,
        description: projectForm.description || `A ${selectedTemplate.name} project`,
        language: selectedLanguage.id,
        template_id: selectedTemplate.id,
        github_username: projectForm.github_username
      });

      clearInterval(progressInterval);
      setLoadingProgress(100);

      if (response.data.success) {
        toast.success(
          <div className="flex flex-col gap-2">
            <span className="font-semibold">🎉 Project Generated Successfully!</span>
            <span>{response.data.message}</span>
            <div className="flex gap-2 mt-2">
              <a 
                href={response.data.repository_url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-blue-500 hover:text-blue-700 flex items-center gap-1 text-sm"
              >
                <ExternalLink className="w-4 h-4" />
                View Repository
              </a>
              <button
                onClick={() => copyToClipboard(response.data.repository_url)}
                className="text-gray-500 hover:text-gray-700 flex items-center gap-1 text-sm"
              >
                <Copy className="w-4 h-4" />
                Copy URL
              </button>
            </div>
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
      clearInterval(progressInterval);
      setLoadingProgress(0);
      const errorMessage = error.response?.data?.detail || "Failed to generate project";
      toast.error(
        <div className="flex flex-col gap-1">
          <span className="font-semibold">❌ Generation Failed</span>
          <span>{errorMessage}</span>
        </div>
      );
    } finally {
      setIsGenerating(false);
      setTimeout(() => setLoadingProgress(0), 2000);
    }
  };

  return (
    <div className={`min-h-screen transition-colors duration-300 ${
      isDarkMode 
        ? 'bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900' 
        : 'bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100'
    }`}>
      {/* Header */}
      <header className={`border-b backdrop-blur-lg sticky top-0 z-50 transition-colors duration-300 ${
        isDarkMode 
          ? 'border-slate-700 bg-slate-900/80' 
          : 'border-white/20 bg-white/80'
      }`}>
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-xl flex items-center justify-center">
                <Code className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className={`text-2xl font-bold bg-gradient-to-r from-blue-700 to-indigo-700 bg-clip-text text-transparent`}>
                  Scaffold Forge
                </h1>
                <p className={`text-sm ${isDarkMode ? 'text-slate-400' : 'text-slate-600'}`}>
                  Template Generator System
                </p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              {/* Stats */}
              <div className="hidden md:flex items-center gap-4">
                <div className="flex items-center gap-1">
                  <TrendingUp className="w-4 h-4 text-green-500" />
                  <span className={`text-sm ${isDarkMode ? 'text-slate-300' : 'text-slate-600'}`}>
                    {stats.totalProjects} projects
                  </span>
                </div>
                <div className="flex items-center gap-1">
                  <Users className="w-4 h-4 text-blue-500" />
                  <span className={`text-sm ${isDarkMode ? 'text-slate-300' : 'text-slate-600'}`}>
                    {stats.totalTemplates} templates
                  </span>
                </div>
              </div>
              
              {/* Dark Mode Toggle */}
              <div className="flex items-center gap-2">
                <Sun className={`w-4 h-4 ${isDarkMode ? 'text-slate-400' : 'text-yellow-500'}`} />
                <Switch
                  checked={isDarkMode}
                  onCheckedChange={toggleTheme}
                  className="data-[state=checked]:bg-slate-600"
                />
                <Moon className={`w-4 h-4 ${isDarkMode ? 'text-blue-400' : 'text-slate-400'}`} />
              </div>
              
              <div className="flex items-center gap-2">
                <Github className={`w-5 h-5 ${isDarkMode ? 'text-slate-400' : 'text-slate-600'}`} />
                <span className={`text-sm ${isDarkMode ? 'text-slate-400' : 'text-slate-600'}`}>
                  Powered by GitHub
                </span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-8">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium mb-6 transition-colors duration-300 ${
            isDarkMode 
              ? 'bg-blue-900/50 text-blue-300 border border-blue-700' 
              : 'bg-blue-100 text-blue-800'
          }`}>
            <Zap className="w-4 h-4" />
            Similar to Santander Gluon
          </div>
          <h2 className={`text-4xl font-bold mb-4 transition-colors duration-300 ${
            isDarkMode ? 'text-white' : 'text-slate-800'
          }`}>
            Generate Projects in Seconds
          </h2>
          <p className={`text-xl max-w-2xl mx-auto transition-colors duration-300 ${
            isDarkMode ? 'text-slate-300' : 'text-slate-600'
          }`}>
            Create professional project scaffolds with GitHub integration. Choose from Java and .NET templates with CI/CD ready configurations.
          </p>
          
          {/* Loading Progress */}
          {loadingProgress > 0 && loadingProgress < 100 && (
            <div className="mt-6 max-w-md mx-auto">
              <div className="flex items-center justify-between mb-2">
                <span className={`text-sm ${isDarkMode ? 'text-slate-400' : 'text-slate-600'}`}>
                  Loading...
                </span>
                <span className={`text-sm ${isDarkMode ? 'text-slate-400' : 'text-slate-600'}`}>
                  {loadingProgress}%
                </span>
              </div>
              <Progress value={loadingProgress} className="h-2" />
            </div>
          )}
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Main Generator */}
          <div className="lg:col-span-2">
            <Card className={`shadow-xl border-0 backdrop-blur-sm transition-colors duration-300 ${
              isDarkMode 
                ? 'bg-slate-800/70 border-slate-700' 
                : 'bg-white/70'
            }`}>
              <CardHeader>
                <CardTitle className={`flex items-center gap-2 transition-colors duration-300 ${
                  isDarkMode ? 'text-white' : 'text-slate-900'
                }`}>
                  <Rocket className="w-5 h-5 text-blue-600" />
                  Project Generator
                </CardTitle>
                <CardDescription className={`transition-colors duration-300 ${
                  isDarkMode ? 'text-slate-400' : 'text-slate-600'
                }`}>
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
                      {languages && languages.length > 0 ? languages.map((language) => (
                        <Card 
                          key={language.id}
                          className={`cursor-pointer transition-all hover:shadow-lg ${
                            selectedLanguage?.id === language.id 
                              ? `ring-2 ring-blue-500 ${isDarkMode ? 'bg-blue-900/30' : 'bg-blue-50'}` 
                              : `hover:${isDarkMode ? 'bg-slate-700' : 'bg-slate-50'}`
                          }`}
                          onClick={() => handleLanguageSelect(language)}
                        >
                          <CardContent className="p-6">
                            <div className="flex items-center gap-3">
                              <span className="text-2xl">{language.icon}</span>
                              <div className="flex-1">
                                <h3 className={`font-semibold text-lg transition-colors duration-300 ${
                                  isDarkMode ? 'text-white' : 'text-slate-900'
                                }`}>
                                  {language.name}
                                </h3>
                                <p className={`text-sm transition-colors duration-300 ${
                                  isDarkMode ? 'text-slate-400' : 'text-slate-600'
                                }`}>
                                  {language.description}
                                </p>
                              </div>
                              {selectedLanguage?.id === language.id && (
                                <CheckCircle className="w-5 h-5 text-blue-600" />
                              )}
                            </div>
                          </CardContent>
                        </Card>
                      )) : (
                        <div className="col-span-2 space-y-4">
                          {[1, 2].map((i) => (
                            <Card key={i} className={`${isDarkMode ? 'bg-slate-800' : 'bg-slate-50'}`}>
                              <CardContent className="p-6">
                                <div className="flex items-center gap-3">
                                  <Skeleton className="w-8 h-8 rounded" />
                                  <div className="flex-1 space-y-2">
                                    <Skeleton className="h-4 w-32" />
                                    <Skeleton className="h-3 w-48" />
                                  </div>
                                </div>
                              </CardContent>
                            </Card>
                          ))}
                        </div>
                      )}
                    </div>
                  </TabsContent>

                  <TabsContent value="template" className="mt-6">
                    <div className="grid md:grid-cols-2 gap-4">
                      {templates && templates.length > 0 ? templates.map((template) => (
                        <Card 
                          key={template.id}
                          className={`cursor-pointer transition-all hover:shadow-lg ${
                            selectedTemplate?.id === template.id 
                              ? `ring-2 ring-blue-500 ${isDarkMode ? 'bg-blue-900/30' : 'bg-blue-50'}` 
                              : `hover:${isDarkMode ? 'bg-slate-700' : 'bg-slate-50'}`
                          }`}
                          onClick={() => handleTemplateSelect(template)}
                        >
                          <CardContent className="p-6">
                            <div className="flex justify-between items-start mb-3">
                              <h3 className={`font-semibold text-lg transition-colors duration-300 ${
                                isDarkMode ? 'text-white' : 'text-slate-900'
                              }`}>
                                {template.name}
                              </h3>
                              <Badge variant="secondary" className={isDarkMode ? 'bg-slate-700 text-slate-300' : ''}>
                                {template.type}
                              </Badge>
                            </div>
                            <p className={`text-sm mb-3 transition-colors duration-300 ${
                              isDarkMode ? 'text-slate-400' : 'text-slate-600'
                            }`}>
                              {template.description}
                            </p>
                            {selectedTemplate?.id === template.id && (
                              <CheckCircle className="w-5 h-5 text-blue-600" />
                            )}
                          </CardContent>
                        </Card>
                      )) : (
                        <div className="col-span-2">
                          {selectedLanguage ? (
                            <div className="space-y-4">
                              {[1, 2, 3].map((i) => (
                                <Card key={i} className={`${isDarkMode ? 'bg-slate-800' : 'bg-slate-50'}`}>
                                  <CardContent className="p-6">
                                    <div className="space-y-3">
                                      <div className="flex justify-between items-start">
                                        <Skeleton className="h-5 w-32" />
                                        <Skeleton className="h-6 w-16 rounded-full" />
                                      </div>
                                      <Skeleton className="h-4 w-full" />
                                      <Skeleton className="h-4 w-3/4" />
                                    </div>
                                  </CardContent>
                                </Card>
                              ))}
                            </div>
                          ) : (
                            <div className={`text-center py-8 transition-colors duration-300 ${
                              isDarkMode ? 'text-slate-400' : 'text-slate-500'
                            }`}>
                              Select a language first
                            </div>
                          )}
                        </div>
                      )}
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
                        <Alert className={isDarkMode ? 'bg-slate-800 border-slate-700' : ''}>
                          <Settings className="h-4 w-4" />
                          <AlertDescription className={isDarkMode ? 'text-slate-300' : ''}>
                            Creating a <strong>{selectedTemplate.name}</strong> project in <strong>{selectedLanguage.name}</strong>
                            {projectForm.name && ` named "${projectForm.name}"`}
                          </AlertDescription>
                        </Alert>
                      )}

                      {/* Progress Bar for Generation */}
                      {isGenerating && (
                        <div className="space-y-2">
                          <div className="flex items-center justify-between">
                            <span className={`text-sm ${isDarkMode ? 'text-slate-400' : 'text-slate-600'}`}>
                              Generating your project...
                            </span>
                            <span className={`text-sm ${isDarkMode ? 'text-slate-400' : 'text-slate-600'}`}>
                              {loadingProgress}%
                            </span>
                          </div>
                          <Progress value={loadingProgress} className="h-2" />
                        </div>
                      )}

                      <Button 
                        onClick={generateProject}
                        disabled={isGenerating || !projectForm.name || !projectForm.github_username}
                        className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 disabled:opacity-50"
                        size="lg"
                      >
                        {isGenerating ? (
                          <>
                            <Loader2 className="w-4 h-4 mr-2 animate-spin" />
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
            <Card className={`shadow-lg border-0 backdrop-blur-sm transition-colors duration-300 ${
              isDarkMode ? 'bg-slate-800/70 border-slate-700' : 'bg-white/70'
            }`}>
              <CardHeader>
                <CardTitle className={`flex items-center gap-2 text-lg transition-colors duration-300 ${
                  isDarkMode ? 'text-white' : 'text-slate-900'
                }`}>
                  <Github className="w-5 h-5 text-slate-600" />
                  Recent Projects
                </CardTitle>
              </CardHeader>
              <CardContent>
                {recentProjects.length > 0 ? (
                  <div className="space-y-3">
                    {recentProjects.map((project, index) => (
                      <div key={index} className={`p-3 rounded-lg transition-colors duration-300 ${
                        isDarkMode ? 'bg-slate-700 hover:bg-slate-600' : 'bg-slate-50 hover:bg-slate-100'
                      }`}>
                        <div className="flex justify-between items-start">
                          <div className="flex-1">
                            <h4 className={`font-medium text-sm transition-colors duration-300 ${
                              isDarkMode ? 'text-white' : 'text-slate-900'
                            }`}>
                              {project.name}
                            </h4>
                            <p className={`text-xs transition-colors duration-300 ${
                              isDarkMode ? 'text-slate-400' : 'text-slate-600'
                            }`}>
                              {project.language}
                            </p>
                          </div>
                          <div className="flex items-center gap-2">
                            <Badge variant="outline" className={`text-xs ${
                              isDarkMode ? 'border-slate-600 text-slate-300' : ''
                            }`}>
                              {new Date(project.created_at).toLocaleDateString()}
                            </Badge>
                            <Button
                              size="sm"
                              variant="ghost"
                              className="h-6 w-6 p-0"
                              onClick={() => copyToClipboard(`https://github.com/${project.github_username}/${project.name}`)}
                            >
                              <Copy className="w-3 h-3" />
                            </Button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-4">
                    <div className={`w-12 h-12 mx-auto mb-3 rounded-full flex items-center justify-center ${
                      isDarkMode ? 'bg-slate-700' : 'bg-slate-100'
                    }`}>
                      <Github className={`w-6 h-6 ${isDarkMode ? 'text-slate-400' : 'text-slate-500'}`} />
                    </div>
                    <p className={`text-sm transition-colors duration-300 ${
                      isDarkMode ? 'text-slate-400' : 'text-slate-500'
                    }`}>
                      No projects generated yet
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Features */}
            <Card className={`shadow-lg border-0 backdrop-blur-sm transition-colors duration-300 ${
              isDarkMode ? 'bg-slate-800/70 border-slate-700' : 'bg-white/70'
            }`}>
              <CardHeader>
                <CardTitle className={`text-lg transition-colors duration-300 ${
                  isDarkMode ? 'text-white' : 'text-slate-900'
                }`}>
                  Features
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex items-center gap-3">
                    <CheckCircle className="w-4 h-4 text-green-600" />
                    <span className={`text-sm transition-colors duration-300 ${
                      isDarkMode ? 'text-slate-300' : 'text-slate-700'
                    }`}>
                      GitHub Integration
                    </span>
                  </div>
                  <div className="flex items-center gap-3">
                    <CheckCircle className="w-4 h-4 text-green-600" />
                    <span className={`text-sm transition-colors duration-300 ${
                      isDarkMode ? 'text-slate-300' : 'text-slate-700'
                    }`}>
                      CI/CD Workflows
                    </span>
                  </div>
                  <div className="flex items-center gap-3">
                    <CheckCircle className="w-4 h-4 text-green-600" />
                    <span className={`text-sm transition-colors duration-300 ${
                      isDarkMode ? 'text-slate-300' : 'text-slate-700'
                    }`}>
                      Ready-to-use Templates
                    </span>
                  </div>
                  <div className="flex items-center gap-3">
                    <CheckCircle className="w-4 h-4 text-green-600" />
                    <span className={`text-sm transition-colors duration-300 ${
                      isDarkMode ? 'text-slate-300' : 'text-slate-700'
                    }`}>
                      Auto Project Setup
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Quick Stats */}
            <div className="space-y-4">
              <StatsCard
                title="Total Projects"
                value={stats.totalProjects.toLocaleString()}
                change="+12%"
                changeType="positive"
                icon={Star}
                description="Projects generated this month"
                className={isDarkMode ? 'bg-slate-800/70 border-slate-700' : 'bg-white/70'}
              />
              <StatsCard
                title="Templates"
                value={stats.totalTemplates}
                change="+2"
                changeType="positive"
                icon={Code}
                description="Available templates"
                className={isDarkMode ? 'bg-slate-800/70 border-slate-700' : 'bg-white/70'}
              />
              <StatsCard
                title="Languages"
                value={stats.totalLanguages}
                change="0"
                changeType="neutral"
                icon={Clock}
                description="Supported languages"
                className={isDarkMode ? 'bg-slate-800/70 border-slate-700' : 'bg-white/70'}
              />
            </div>
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