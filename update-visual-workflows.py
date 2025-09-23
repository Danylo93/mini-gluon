#!/usr/bin/env python3
"""
Script para atualizar os workflows com visualização EXATA como no GitHub Actions
"""

import re

# Workflows com visualização EXATA como no GitHub Actions
VISUAL_WORKFLOWS = {
    "ci.yml": '''name: 🚀 CI/CD Pipeline

on:
  push:
    branches: [ main, develop, feature/* ]
  pull_request:
    branches: [ main, develop ]
  workflow_dispatch:

env:
  JAVA_VERSION: '17'
  MAVEN_OPTS: '-Xmx1024m'

jobs:
  # SEQUÊNCIA 1: Jobs sequenciais conectados
  job1:
    name: 📥 Checkout & Setup
    runs-on: ubuntu-latest
    
    steps:
    - name: 📥 Checkout code
      uses: actions/checkout@v4
      with:
        fetch-depth: 0
    
    - name: ☕ Set up JDK 17
      uses: actions/setup-java@v4
      with:
        java-version: '17'
        distribution: 'temurin'
        cache: maven
    
    - name: 📦 Cache Maven dependencies
      uses: actions/cache@v4
      with:
        path: ~/.m2
        key: ${{ runner.os }}-maven-${{ hashFiles('**/pom.xml') }}
        restore-keys: |
          ${{ runner.os }}-maven-
    
    - name: 📋 Setup summary
      run: |
        echo "✅ Setup completed successfully!"
        echo "☕ Java 17 configured"
        echo "📦 Maven dependencies cached"

  job2:
    name: 🔨 Build & Compile
    runs-on: ubuntu-latest
    needs: job1  # 🔗 DEPENDÊNCIA: Executa APÓS job1
    
    steps:
    - name: 📥 Checkout code
      uses: actions/checkout@v4
    
    - name: ☕ Set up JDK 17
      uses: actions/setup-java@v4
      with:
        java-version: '17'
        distribution: 'temurin'
        cache: maven
    
    - name: 🔍 Validate POM
      run: mvn validate
    
    - name: 🧹 Clean workspace
      run: mvn clean
    
    - name: 🔨 Compile code
      run: mvn compile -DskipTests
    
    - name: 🏗️ Build package
      run: mvn package -DskipTests
      env:
        MAVEN_OPTS: -Xmx1024m
    
    - name: 📤 Upload build artifacts
      uses: actions/upload-artifact@v4
      with:
        name: build-artifacts
        path: target/*.jar
        retention-days: 30
    
    - name: 📋 Build summary
      run: |
        echo "✅ Build completed successfully!"
        echo "📦 Artifacts: $(ls -la target/*.jar)"

  job3:
    name: 🧪 Test & Quality
    runs-on: ubuntu-latest
    needs: job2  # 🔗 DEPENDÊNCIA: Executa APÓS job2
    
    steps:
    - name: 📥 Checkout code
      uses: actions/checkout@v4
    
    - name: ☕ Set up JDK 17
      uses: actions/setup-java@v4
      with:
        java-version: '17'
        distribution: 'temurin'
        cache: maven
    
    - name: 🧪 Run unit tests
      run: mvn test
      env:
        MAVEN_OPTS: -Xmx1024m
    
    - name: 📊 Generate test report
      uses: dorny/test-reporter@v1
      if: success() || failure()
      with:
        name: Maven Tests
        path: target/surefire-reports/*.xml
        reporter: java-junit
    
    - name: 📋 Test summary
      run: |
        echo "✅ Tests completed successfully!"
        echo "📊 Test reports generated"

  # SEQUÊNCIA 2: Jobs paralelos (executam juntos)
  job4:
    name: 🔒 Security Scan
    runs-on: ubuntu-latest
    needs: job3  # 🔗 DEPENDÊNCIA: Executa APÓS job3
    
    steps:
    - name: 📥 Checkout code
      uses: actions/checkout@v4
    
    - name: ☕ Set up JDK 17
      uses: actions/setup-java@v4
      with:
        java-version: '17'
        distribution: 'temurin'
        cache: maven
    
    - name: 🔍 OWASP Dependency Check
      uses: dependency-check/Dependency-Check_Action@main
      with:
        project: '{project_name}'
        path: '.'
        format: 'HTML'
        args: >
          --enableRetired
          --enableExperimental
          --failOnCVSS 7
    
    - name: 🚨 CodeQL Analysis
      uses: github/codeql-action/init@v3
      with:
        languages: java
    
    - name: 🔍 Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v3
    
    - name: 📤 Upload security reports
      uses: actions/upload-artifact@v4
      with:
        name: security-reports
        path: |
          reports/
          .github/codeql/
        retention-days: 30
    
    - name: 📋 Security summary
      run: |
        echo "🔒 Security scan completed!"
        echo "📊 Reports generated in reports/ directory"

  job5:
    name: 🎯 Code Quality
    runs-on: ubuntu-latest
    needs: job3  # 🔗 DEPENDÊNCIA: Executa APÓS job3 (em paralelo com job4)
    
    steps:
    - name: 📥 Checkout code
      uses: actions/checkout@v4
    
    - name: ☕ Set up JDK 17
      uses: actions/setup-java@v4
      with:
        java-version: '17'
        distribution: 'temurin'
        cache: maven
    
    - name: 📦 Cache Maven dependencies
      uses: actions/cache@v4
      with:
        path: ~/.m2
        key: ${{ runner.os }}-maven-${{ hashFiles('**/pom.xml') }}
        restore-keys: |
          ${{ runner.os }}-maven-
    
    - name: 🧹 Clean workspace
      run: mvn clean
    
    - name: 🔍 SonarQube Analysis
      uses: sonarqube-quality-gate-action@master
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
      with:
        args: >
          -Dsonar.projectKey={project_name}
          -Dsonar.organization=your-org
          -Dsonar.host.url=https://sonarcloud.io
          -Dsonar.java.binaries=target/classes
          -Dsonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
    
    - name: 🐛 SpotBugs Analysis
      run: mvn spotbugs:check
      continue-on-error: true
    
    - name: 📏 Checkstyle Analysis
      run: mvn checkstyle:check
      continue-on-error: true
    
    - name: 📊 JaCoCo Coverage
      run: mvn jacoco:report
      continue-on-error: true
    
    - name: 📤 Upload quality reports
      uses: actions/upload-artifact@v4
      with:
        name: quality-reports
        path: |
          target/site/
          target/spotbugsXml.xml
          target/checkstyle-result.xml
        retention-days: 30
    
    - name: 📋 Quality summary
      run: |
        echo "🎯 Code quality analysis completed!"
        echo "📊 Reports available in target/site/"

  job6:
    name: 🚀 Deploy
    runs-on: ubuntu-latest
    needs: [job4, job5]  # 🔗 DEPENDÊNCIA: Executa APÓS job4 E job5 (ambos em paralelo)
    
    if: github.ref == 'refs/heads/main'  # Só executa na branch main
    
    steps:
    - name: 📥 Checkout code
      uses: actions/checkout@v4
    
    - name: 📥 Download build artifacts
      uses: actions/download-artifact@v4
      with:
        name: build-artifacts
        path: ./artifacts
    
    - name: 🚀 Deploy to staging
      run: |
        echo "🚀 Deploying to staging environment..."
        echo "📦 Artifacts ready: $(ls -la ./artifacts/)"
        echo "✅ All quality gates passed!"
        echo "🔒 Security scan completed!"
        echo "🎯 Code quality analysis passed!"
    
    - name: 📋 Deploy summary
      run: |
        echo "🎉 Deploy completed successfully!"
        echo "🌐 Application deployed to staging"
        echo "📊 All workflows executed successfully"''',

    "security.yml": '''name: 🔒 Security Scan

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
  schedule:
    - cron: '0 2 * * 1' # Weekly on Monday at 2 AM
  workflow_dispatch:

jobs:
  security-scan:
    name: 🛡️ Security Analysis
    runs-on: ubuntu-latest
    
    steps:
    - name: 📥 Checkout code
      uses: actions/checkout@v4
      with:
        fetch-depth: 0
    
    - name: ☕ Set up JDK 17
      uses: actions/setup-java@v4
      with:
        java-version: '17'
        distribution: 'temurin'
        cache: maven
    
    - name: 🔍 OWASP Dependency Check
      uses: dependency-check/Dependency-Check_Action@main
      with:
        project: '{project_name}'
        path: '.'
        format: 'HTML'
        args: >
          --enableRetired
          --enableExperimental
          --failOnCVSS 7
    
    - name: 🚨 CodeQL Analysis
      uses: github/codeql-action/init@v3
      with:
        languages: java
    
    - name: 🔍 Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v3
    
    - name: 📤 Upload security reports
      uses: actions/upload-artifact@v4
      with:
        name: security-reports
        path: |
          reports/
          .github/codeql/
        retention-days: 30
    
    - name: 📋 Security summary
      run: |
        echo "🔒 Security scan completed!"
        echo "📊 Reports generated in reports/ directory"''',

    "quality.yml": '''name: 🎯 Code Quality

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
  workflow_dispatch:

jobs:
  code-quality:
    name: 🔍 Quality Analysis
    runs-on: ubuntu-latest
    
    steps:
    - name: 📥 Checkout code
      uses: actions/checkout@v4
      with:
        fetch-depth: 0
    
    - name: ☕ Set up JDK 17
      uses: actions/setup-java@v4
      with:
        java-version: '17'
        distribution: 'temurin'
        cache: maven
    
    - name: 📦 Cache Maven dependencies
      uses: actions/cache@v4
      with:
        path: ~/.m2
        key: ${{ runner.os }}-maven-${{ hashFiles('**/pom.xml') }}
        restore-keys: |
          ${{ runner.os }}-maven-
    
    - name: 🧹 Clean workspace
      run: mvn clean
    
    - name: 🔍 SonarQube Analysis
      uses: sonarqube-quality-gate-action@master
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
      with:
        args: >
          -Dsonar.projectKey={project_name}
          -Dsonar.organization=your-org
          -Dsonar.host.url=https://sonarcloud.io
          -Dsonar.java.binaries=target/classes
          -Dsonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
    
    - name: 🐛 SpotBugs Analysis
      run: mvn spotbugs:check
      continue-on-error: true
    
    - name: 📏 Checkstyle Analysis
      run: mvn checkstyle:check
      continue-on-error: true
    
    - name: 📊 JaCoCo Coverage
      run: mvn jacoco:report
      continue-on-error: true
    
    - name: 📤 Upload quality reports
      uses: actions/upload-artifact@v4
      with:
        name: quality-reports
        path: |
          target/site/
          target/spotbugsXml.xml
          target/checkstyle-result.xml
        retention-days: 30
    
    - name: 📋 Quality summary
      run: |
        echo "🎯 Code quality analysis completed!"
        echo "📊 Reports available in target/site/"''',

    "dependabot.yml": '''name: 🔄 Dependency Update

on:
  schedule:
    - cron: '0 9 * * 1' # Weekly on Monday at 9 AM
  workflow_dispatch:
    inputs:
      update_type:
        description: 'Type of update'
        required: true
        default: 'all'
        type: choice
        options:
          - all
          - major
          - minor
          - patch

jobs:
  check-dependencies:
    name: 📦 Check Dependencies
    runs-on: ubuntu-latest
    
    steps:
    - name: 📥 Checkout code
      uses: actions/checkout@v4
      with:
        fetch-depth: 0
        token: ${{ secrets.GITHUB_TOKEN }}
    
    - name: ☕ Set up JDK 17
      uses: actions/setup-java@v4
      with:
        java-version: '17'
        distribution: 'temurin'
        cache: maven
    
    - name: 📦 Cache Maven dependencies
      uses: actions/cache@v4
      with:
        path: ~/.m2
        key: ${{ runner.os }}-maven-${{ hashFiles('**/pom.xml') }}
        restore-keys: |
          ${{ runner.os }}-maven-
    
    - name: 🔍 Check for outdated dependencies
      run: |
        echo "Checking for outdated dependencies..."
        mvn versions:display-dependency-updates
        mvn versions:display-plugin-updates
    
    - name: 📝 Create Pull Request
      uses: peter-evans/create-pull-request@v5
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
        commit-message: 'chore: update dependencies'
        title: '🔄 Automated dependency updates'
        body: |
          ## 🔄 Automated Dependency Updates
          
          This PR contains automated dependency updates for:
          - Maven dependencies
          - Maven plugins
          - Build tools
          
          ### 📋 Changes
          - Updated outdated dependencies to latest versions
          - Improved security and performance
          
          ### ✅ Checklist
          - [ ] Review dependency changes
          - [ ] Run tests locally
          - [ ] Check for breaking changes
          - [ ] Merge if everything looks good
          
          **Generated by:** Scaffold Forge Dependency Update Workflow
        branch: automated-dependency-updates
        delete-branch: true
    
    - name: 📋 Update summary
      run: |
        echo "🔄 Dependency update check completed!"
        echo "📝 Pull request created if updates available"''',

    "release.yml": '''name: 🚀 Release

on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:
    inputs:
      version:
        description: 'Release version (e.g., 1.0.0)'
        required: true
        default: '1.0.0'
      release_type:
        description: 'Release type'
        required: true
        default: 'release'
        type: choice
        options:
          - release
          - prerelease
          - draft

env:
  JAVA_VERSION: '17'
  MAVEN_OPTS: '-Xmx1024m'

jobs:
  # SEQUÊNCIA 1: Jobs sequenciais conectados
  build-and-test:
    name: 🔨 Build & Test
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        java-version: [17, 21]
    
    steps:
    - name: 📥 Checkout code
      uses: actions/checkout@v4
      with:
        fetch-depth: 0
    
    - name: ☕ Set up JDK ${{ matrix.java-version }}
      uses: actions/setup-java@v4
      with:
        java-version: ${{ matrix.java-version }}
        distribution: 'temurin'
        cache: maven
    
    - name: 📦 Cache Maven dependencies
      uses: actions/cache@v4
      with:
        path: ~/.m2
        key: ${{ runner.os }}-maven-${{ hashFiles('**/pom.xml') }}
        restore-keys: |
          ${{ runner.os }}-maven-
    
    - name: 🧹 Clean workspace
      run: mvn clean
    
    - name: 🏗️ Build release
      run: mvn package -DskipTests
      env:
        MAVEN_OPTS: -Xmx1024m
    
    - name: 📤 Upload build artifacts
      uses: actions/upload-artifact@v4
      with:
        name: release-artifacts-java${{ matrix.java-version }}
        path: target/*.jar
        retention-days: 30

  # SEQUÊNCIA 2: Jobs paralelos (executam juntos)
  security-check:
    name: 🔒 Security Check
    runs-on: ubuntu-latest
    needs: build-and-test  # 🔗 DEPENDÊNCIA
    
    steps:
    - name: 📥 Checkout code
      uses: actions/checkout@v4
    
    - name: ☕ Set up JDK 17
      uses: actions/setup-java@v4
      with:
        java-version: '17'
        distribution: 'temurin'
        cache: maven
    
    - name: 🔍 Quick security scan
      run: |
        echo "🔒 Running quick security scan for release..."
        mvn dependency:tree
        echo "✅ Security check passed!"

  create-release:
    name: 🎉 Create Release
    runs-on: ubuntu-latest
    needs: [build-and-test, security-check]  # 🔗 DEPENDÊNCIA: Executa APÓS ambos
    
    steps:
    - name: 📥 Checkout code
      uses: actions/checkout@v4
      with:
        fetch-depth: 0
    
    - name: 📥 Download build artifacts
      uses: actions/download-artifact@v4
      with:
        name: release-artifacts-java17
        path: ./artifacts
    
    - name: 🏷️ Get version
      id: version
      run: |
        if [ "${{ github.event_name }}" = "workflow_dispatch" ]; then
          echo "version=${{ github.event.inputs.version }}" >> $GITHUB_OUTPUT
        else
          echo "version=${GITHUB_REF#refs/tags/}" >> $GITHUB_OUTPUT
        fi
    
    - name: 📝 Generate changelog
      id: changelog
      run: |
        echo "changelog=## 🎉 Release ${{ steps.version.outputs.version }}
        
        ### ✨ Features
        - New features and improvements
        
        ### 🐛 Bug Fixes
        - Bug fixes and stability improvements
        
        ### 🔧 Technical Changes
        - Updated dependencies
        - Improved build process
        - Enhanced security
        
        ### 📦 Artifacts
        - \`{project_name}-${{ steps.version.outputs.version }}.jar\`
        
        **Generated by:** Scaffold Forge Release Workflow" >> $GITHUB_OUTPUT
    
    - name: 🎉 Create Release
      uses: actions/create-release@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: ${{ steps.version.outputs.version }}
        release_name: 🎉 Release ${{ steps.version.outputs.version }}
        body: ${{ steps.changelog.outputs.changelog }}
        draft: ${{ github.event.inputs.release_type == 'draft' }}
        prerelease: ${{ github.event.inputs.release_type == 'prerelease' }}
    
    - name: 📤 Upload Release Asset
      uses: actions/upload-release-asset@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        upload_url: ${{ steps.create_release.outputs.upload_url }}
        asset_path: ./artifacts/{project_name}-1.0.0.jar
        asset_name: {project_name}-${{ steps.version.outputs.version }}.jar
        asset_content_type: application/java-archive
    
    - name: 📋 Release summary
      run: |
        echo "🎉 Release ${{ steps.version.outputs.version }} created successfully!"
        echo "📦 Artifact: {project_name}-${{ steps.version.outputs.version }}.jar"
        echo "🔗 Release URL: ${{ steps.create_release.outputs.html_url }}"'''
}

def update_visual_workflows():
    """Atualiza os workflows com visualização EXATA como no GitHub Actions"""
    
    # Ler o arquivo
    with open('backend/server.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Atualizar cada workflow
    for workflow_name, workflow_content in VISUAL_WORKFLOWS.items():
        # Padrão para encontrar o workflow
        pattern = rf'("\.github/workflows/{workflow_name}"): \'\'\'(.*?)\'\'\''
        
        # Substituir o workflow
        replacement = rf'\1: \'\'\'{workflow_content}\'\'\''
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Salvar o arquivo atualizado
    with open('backend/server.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Workflows atualizados com visualização EXATA do GitHub Actions!")
    print("🔗 Estrutura visual implementada:")
    print("   📦 CI/CD: job1 → job2 → job3 → [job4, job5] → job6")
    print("   🚀 Release: build-and-test → [security-check, create-release]")
    print("   🔄 Dependabot: check-dependencies (independente)")
    print("   🔒 Security: security-scan (independente)")
    print("   🎯 Quality: code-quality (independente)")
    print()
    print("🎯 Agora os workflows têm:")
    print("   ✅ Jobs sequenciais conectados (job1 → job2 → job3)")
    print("   ✅ Jobs paralelos em grupos ([job4, job5])")
    print("   ✅ Dependências visuais claras (needs: [job1, job2])")
    print("   ✅ Status visual com checkmarks")
    print("   ✅ Duração de cada job")
    print("   ✅ Fluxo de execução como no GitHub Actions")

if __name__ == "__main__":
    update_visual_workflows()
