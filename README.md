<<<<<<< HEAD
# AspireHR - Modern HR and Payroll Management System

<div align="center">
  <img src="https://img.shields.io/badge/Version-1.0.0--dev-blue" alt="Version">
  <img src="https://img.shields.io/badge/Framework-Frappe-green" alt="Framework">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
  <img src="https://img.shields.io/badge/Python-3.8+-blue" alt="Python Version">
</div>

## 🚀 Overview

AspireHR is a comprehensive Human Resources and Payroll Management System built on the powerful Frappe Framework. It provides all the essential HR functionalities needed to manage your workforce effectively with modern, intuitive interfaces and powerful automation capabilities.

## ✨ Key Features

### 🏢 **Core HR Management**
- **Employee Lifecycle Management** - From onboarding to separation
- **Department & Designation Management** - Organize workforce hierarchies
- **Employee Self-Service Portal** - Empower employees with self-service capabilities
- **Document Management** - Centralized employee document storage

### 📅 **Attendance & Leave Management**
- **Multi-Channel Attendance Tracking** - Biometric, manual, and mobile check-in
- **Dynamic Leave Allocation** - 🎯 **NEW!** Allocate leaves on custom dates
- **Advanced Leave Policies** - Flexible leave types and approval workflows
- **Shift Management** - Complex shift patterns and scheduling
- **Holiday Management** - Company-wide and location-specific calendars

### 💰 **Payroll Management**
- **Flexible Salary Structures** - Customizable earnings and deductions
- **Automated Payroll Processing** - One-click payroll generation
- **Tax Compliance** - Built-in tax calculations and statutory compliance
- **Detailed Salary Slips** - Comprehensive salary breakdowns
- **Multi-currency Support** - Global payroll processing

### 📊 **Performance Management**
- **360-Degree Appraisals** - Comprehensive performance reviews
- **Goal Setting & Tracking** - OKR and KPI management
- **Performance Analytics** - Data-driven insights and reports
- **Competency Management** - Skills tracking and development

### 🎯 **Recruitment & Training**
- **Job Opening Management** - End-to-end recruitment process
- **Applicant Tracking System** - Streamlined hiring pipeline
- **Interview Scheduling** - Automated interview coordination
- **Training Programs** - Employee development and learning management

### 💳 **Expense Management**
- **Digital Expense Claims** - Mobile-first expense submission
- **Automated Approval Workflows** - Streamlined expense processing
- **Travel Management** - Comprehensive travel planning and tracking
- **Reimbursement Processing** - Fast and accurate reimbursements

### 📈 **Analytics & Reporting**
- **Real-time HR Dashboard** - Live metrics and KPIs
- **Advanced Analytics** - Deep insights into HR data
- **Compliance Reporting** - Regulatory and statutory reports
- **Custom Report Builder** - Build reports without coding

## 🎯 **Dynamic Leave Allocation - Featured Capability**

Our advanced leave allocation system allows you to:

- ✅ **Allocate leaves on any custom date** - Not just calendar years
- ✅ **Bulk allocation via CSV upload** - Process hundreds of employees at once
- ✅ **Carry forward unused leaves** - Automatic calculation from previous periods
- ✅ **Adjust existing allocations** - Add or subtract leaves with full audit trail
- ✅ **Real-time validation** - Prevent errors before processing
- ✅ **Automated scheduling** - Annual and monthly allocations
- ✅ **Balance inquiry** - Check leave balances on any date
- ✅ **Comprehensive APIs** - Integration-ready endpoints

## 🛠️ **Installation**

### Prerequisites
- Frappe Framework (v14 or higher)
- ERPNext (v14 or higher)
- Python 3.8+
- Node.js 14+
- Git

### Quick Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/innopay-suresh/AspireHR.git
   cd AspireHR
   ```

2. **Install in Frappe environment**
   ```bash
   bench get-app /path/to/AspireHR
   bench --site [your-site-name] install-app aspirehr
   bench restart
   ```

3. **Setup and configuration**
   ```bash
   bench --site [your-site-name] migrate
   bench --site [your-site-name] build
   ```

### Development Setup

```bash
# Clone repository
git clone https://github.com/innopay-suresh/AspireHR.git

# Install dependencies
pip install -r requirements.txt

# The app includes mock implementations for development
# See DEVELOPMENT_SETUP.md for detailed instructions
```

## 📱 **Quick Start**

### 1. Initial Configuration
- Configure HR Settings and company information
- Set up leave types and salary components
- Create departments and designations
- Configure user roles and permissions

### 2. Employee Setup
- Import or create employee records
- Set up salary structures
- Assign leave policies
- Configure reporting hierarchies

### 3. Dynamic Leave Allocation
```javascript
// Via JavaScript API
aspirehr.leave_allocation.show_allocation_dialog();

// Via REST API
POST /api/method/aspirehr.api.leave_allocation.allocate_employee_leaves
{
    "employee": "EMP-001",
    "leave_type": "Annual Leave",
    "allocation_date": "2024-01-01",
    "new_leaves_allocated": 21,
    "carry_forward": true
}
```

## 🔧 **Configuration**

### Leave Types Setup
```python
# Configure earned leave types
leave_type = frappe.get_doc("Leave Type", "Annual Leave")
leave_type.is_earned_leave = 1
leave_type.earned_leave_frequency = "Monthly"
leave_type.max_carry_forwarded_leaves = 5
leave_type.save()
```

### Automated Schedules
- **Annual Allocation**: January 1st, 2:00 AM
- **Monthly Allocation**: 1st of every month, 2:00 AM
- **Custom Schedules**: Configurable via cron expressions

## 📊 **API Documentation**

### Leave Allocation Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/method/aspirehr.api.leave_allocation.allocate_employee_leaves` | POST | Allocate leaves dynamically |
| `/api/method/aspirehr.api.leave_allocation.bulk_allocate_leaves` | POST | Bulk allocation via CSV/JSON |
| `/api/method/aspirehr.api.leave_allocation.adjust_employee_leave_allocation` | POST | Adjust existing allocations |
| `/api/method/aspirehr.api.leave_allocation.get_employee_leave_balance` | GET | Check leave balances |

### Example Usage
```bash
# Allocate leaves to all employees
curl -X POST "https://your-site.com/api/method/aspirehr.api.leave_allocation.allocate_employee_leaves" \
  -H "Content-Type: application/json" \
  -d '{
    "leave_type": "Annual Leave",
    "allocation_date": "2024-01-01",
    "new_leaves_allocated": 21,
    "carry_forward": true
  }'
```

## 🎨 **User Interface**

### Desktop Interface
- Modern, responsive design
- Intuitive navigation and workflows
- Real-time updates and notifications
- Customizable dashboards

### Mobile Interface
- Mobile-first design
- Offline capability for attendance
- Quick actions and approvals
- Push notifications

## 🔐 **Security & Permissions**

### Role-Based Access Control
- **HR Manager**: Full access to all HR functions
- **HR User**: Limited HR functions for executives
- **Employee**: Self-service access only
- **Leave Approver**: Leave approval permissions
- **Payroll Manager**: Payroll processing access

### Data Security
- Row-level security for sensitive data
- Audit trails for all transactions
- Encryption for sensitive information
- Regular security updates

## 🧪 **Testing**

```bash
# Run unit tests
bench --site [your-site-name] run-tests --app aspirehr

# Run specific test
bench --site [your-site-name] run-tests --app aspirehr --module "aspirehr.tests.test_leave_allocation"

# Run integration tests
bench --site [your-site-name] run-tests --app aspirehr --integration
```

## 📈 **Performance**

### Optimization Features
- Database indexing for fast queries
- Caching for frequently accessed data
- Background job processing
- Efficient bulk operations

### Scalability
- Supports 1000+ employees
- Multi-company architecture
- Distributed deployment ready
- Cloud-native design

## 🤝 **Contributing**

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting pull requests.

### Development Process
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

### Code Standards
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings for functions
- Include unit tests for new features

## 📚 **Documentation**

- [User Manual](docs/user_manual.md)
- [Administrator Guide](docs/admin_guide.md)
- [API Documentation](docs/api_docs.md)
- [Development Setup](DEVELOPMENT_SETUP.md)
- [Dynamic Leave Allocation Guide](docs/dynamic_leave_allocation.md)

## 🐛 **Support**

### Community Support
- [GitHub Issues](https://github.com/innopay-suresh/AspireHR/issues)
- [Discussion Forum](https://github.com/innopay-suresh/AspireHR/discussions)
- [Wiki](https://github.com/innopay-suresh/AspireHR/wiki)

### Professional Support
For enterprise support and customization services:
- Email: suresh@innopay.com
- Website: [innopay.com](https://innopay.com)

## 📋 **Roadmap**

### v1.1.0 (Q3 2024)
- [ ] Advanced analytics dashboard
- [ ] AI-powered resume screening
- [ ] WhatsApp integration
- [ ] Advanced reporting with charts

### v1.2.0 (Q4 2024)
- [ ] Multi-currency payroll
- [ ] Advanced shift patterns
- [ ] Learning management system
- [ ] Workflow automation

### v2.0.0 (2025)
- [ ] Mobile app
- [ ] AI-powered insights
- [ ] Advanced integrations
- [ ] Multi-tenant architecture

## � **Troubleshooting**

### Asset Building Issues

If you encounter errors during asset building (esbuild errors), try these solutions:

1. **Install without building assets:**
   ```bash
   bench get-app https://github.com/innopay-suresh/commi.git
   bench --site [your-site-name] install-app aspirehr --skip-assets
   bench --site [your-site-name] migrate
   ```

2. **Build assets separately:**
   ```bash
   bench build --app aspirehr
   ```

3. **Alternative installation script:**
   ```bash
   # Download and run the installation script
   curl -O https://raw.githubusercontent.com/innopay-suresh/commi/main/install_without_assets.sh
   chmod +x install_without_assets.sh
   ./install_without_assets.sh
   ```

### Common Issues

- **Missing dependencies**: Make sure Frappe Framework is properly installed
- **Permission errors**: Check file permissions in the apps directory
- **Build errors**: Try clearing the cache with `bench clear-cache`

## �📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- Built on the robust [Frappe Framework](https://frappeframework.com)
- Inspired by [ERPNext](https://erpnext.com) architecture
- Thanks to the open-source community for contributions

---

<div align="center">
  <p><strong>AspireHR</strong> - Empowering Organizations with Modern HR Solutions</p>
  <p>⭐ Star this repository if you find it helpful!</p>
</div>
=======
# AspireHR
>>>>>>> 131187f5385ee7d7f819daf89b91282a438c483f
