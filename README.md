# App Rating Analysis System

A comprehensive web application for analyzing and predicting app ratings across multiple datasets. This system provides insights into app performance, ratings, and trends across different versions and categories.

## Features

- **Multi-Dataset Analysis**: Process and analyze app data from multiple CSV sources
- **Rating Analytics**: 
  - Average ratings across all versions
  - Version count tracking
  - Highest achieved ratings
- **Advanced Search**:
  - Instant app search with consolidated results
  - Category-based filtering
- **Comprehensive App Information**:
  - Price (with USD to INR conversion)
  - App size
  - Download counts
  - Version tracking
  - Category classification

## Technical Stack

- **Backend**: Python 3.11 with Flask 2.3.3
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Processing**: Pandas
- **UI Framework**: Bootstrap 5.1.3
- **Icons**: Font Awesome

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/app-rating-system.git
cd app-rating-system
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Place your CSV data files in the `data` directory. Files should have the following columns:
   - App Name
   - App Size
   - App Price
   - App Type
   - App Version
   - User Rating
   - Downloads

5. Run the application:
```bash
python app.py
```

6. Open your browser and navigate to: `http://localhost:3000`

## Project Structure

```
app_rating_system/
├── app.py              # Main Flask application
├── data/               # CSV data files directory
├── static/
│   ├── style.css      # Custom CSS styles
│   └── script.js      # Frontend JavaScript
├── templates/
│   └── index.html     # Main HTML template
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```

## Data Format

The system expects CSV files with the following columns:
- `App Name`: Name of the application
- `App Size`: Size of the app (in MB or KB)
- `App Price`: Price in USD (or "Free")
- `App Type`: Category/type of the app
- `App Version`: Version number
- `User Rating`: Rating from 1 to 5
- `Downloads`: Number of downloads

## Features in Detail

1. **Data Processing**:
   - Handles multiple CSV files
   - Cleans and standardizes data
   - Converts prices to INR
   - Normalizes app sizes to MB

2. **Rating Analysis**:
   - Calculates average ratings across versions
   - Tracks version history
   - Identifies peak ratings

3. **Search Functionality**:
   - Real-time search results
   - Shows best-matching results
   - Provides comprehensive app details

4. **Category Management**:
   - Filters apps by category
   - Shows top apps per category
   - Maintains category-wise statistics

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask framework
- Pandas library
- Bootstrap team
- Font Awesome
