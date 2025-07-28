# YT Comment Reply AI Bot

An intelligent YouTube comment reply automation system that uses AI to generate contextual replies to comments automatically. This YT comment AI bot helps automate YouTube comment responses with machine learning.

## 🎯 Project Overview

This YT comment reply AI bot combines machine learning with GUI automation to:
- **Analyze YouTube comments** using a trained AI model for comment analysis
- **Generate intelligent replies** based on comment context with AI-powered responses
- **Automate YouTube comment interactions** (like, heart, reply) for content creators
- **Provide multiple interfaces** (GUI, CLI, Server) for YouTube comment automation

## 🏗️ Architecture

### AI Model
- **Encoder-Decoder Architecture** with attention mechanism
- **GRU-based sequence-to-sequence** model
- **TensorFlow/Keras** implementation
- **Custom tokenization** for text processing

### Components
- **GUI Application** - Modern interface with CustomTkinter
- **YouTube Bot** - PyAutoGUI automation for browser interaction
- **HTTP Server** - API endpoint for external integrations
- **Training System** - Model retraining capabilities

## 📁 Project Structure

```
comment/
├── main.py                 # Entry point - handles all modes
├── gui_app.py             # GUI interface with controls
├── botserver.py           # HTTP server for API access
├── startytbot.py          # YouTube automation bot
├── starttraining.py       # Model training script
├── data_preprocessing.py  # Text cleaning and processing
├── model/                 # AI model implementation
│   ├── model.py          # Encoder/Decoder classes
│   ├── tokenization.py   # Text tokenization
│   └── train.py          # Training logic
├── data/                  # Training data and model weights
│   ├── encoder_weights.h5 # Trained encoder weights
│   ├── decoder_weights.h5 # Trained decoder weights
│   ├── inp_lang.pkl      # Input tokenizer
│   ├── targ_lang.pkl     # Target tokenizer
│   └── trainingdata/     # Training datasets
├── ytbot/                 # YouTube bot components
│   ├── commentmodel.py   # Model inference wrapper
│   └── popupwindow.py    # User interaction popup
└── utils/                 # Utility functions
    ├── utils.py          # General utilities
    ├── usage.py          # Usage tracking
    └── mouselocation.py  # Mouse position helper
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.9+
- Windows OS (for automation features)

### Option 1: Interactive Setup (Recommended)
```bash
python setup.py
```
Choose from:
- **Pip + Virtual Environment** (No conda needed)
- **Conda Environment** (If you have conda)
- **Global Installation** (Quick but not isolated)

### Option 2: Manual Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

### Option 3: Conda Environment
```bash
# Create conda environment
conda env create -f environment.yml
conda activate yt-comment-reply-ai-bot
python main.py
```

### Option 4: Docker (Advanced)
```bash
# Build and run
docker-compose up commentbot

# Or build manually
docker build -t commentbot .
docker run -p 65432:65432 commentbot
```

## 💻 Usage

### GUI Mode (Default)
```bash
python main.py
```
- **Modern interface** with dark/light themes
- **Server control** toggle
- **Comment testing** functionality
- **Training controls** with password protection
- **Real-time logging**

### Bot Mode
```bash
python main.py bot
```
- **Automated YouTube interaction**
- **Comment processing** and reply generation
- **User confirmation** via popup windows
- **Action logging** to dataset

### Server Mode
```bash
python main.py server
```
- **HTTP API** on localhost:65432
- **CORS enabled** for web integration
- **Simple text-in, reply-out** interface

### Training Mode
```bash
python main.py train
```
- **Model retraining** on new data
- **TensorBoard logging** for monitoring
- **Automatic weight saving**

## 🤖 AI Model Details

### Architecture
- **Encoder**: GRU-based with embedding layer
- **Decoder**: GRU with Bahdanau attention mechanism
- **Attention**: Context-aware reply generation
- **Tokenization**: Custom word-level tokenizers

### Training Data Format
```
comment_text	reply_text	status
Hello there	Hi! Thanks for watching	normal
Great video	Glad you enjoyed it!	normal
```

### Model Parameters
- **Embedding Dimension**: 256
- **Hidden Units**: 512
- **Max Input Length**: 38 tokens
- **Max Output Length**: 59 tokens
- **Batch Size**: 16 (training), 1 (inference)

## 🔧 Configuration

### YouTube Bot Coordinates
Edit `startytbot.py` to adjust screen coordinates for your setup:
```python
# Navigation coordinates (adjust for your screen)
pyautogui.moveTo(139, 143, duration=0.5)  # First button
pyautogui.moveTo(135, 667, duration=0.5)  # Second button
```

### Training Password
Change in `gui_app.py`:
```python
self.training_password = "your_password_here"
```

### Server Configuration
Modify in `botserver.py`:
```python
def start_server(stop_event, host='127.0.0.1', port=65432):
```

## 📊 Features

### GUI Features
- ✅ **Server Control** - Start/stop HTTP server
- ✅ **Theme Toggle** - Dark/light mode
- ✅ **Comment Testing** - Test model responses
- ✅ **Activity Logging** - Real-time operation logs
- ✅ **Status Monitoring** - Component status indicators

### Bot Features
- ✅ **Smart Comment Detection** - Filters and processes comments
- ✅ **AI Reply Generation** - Context-aware responses
- ✅ **User Confirmation** - Popup for manual approval
- ✅ **Action Automation** - Like, heart, reply actions
- ✅ **Data Collection** - Logs interactions for training

### API Features
- ✅ **HTTP Endpoint** - Simple POST requests
- ✅ **CORS Support** - Web integration ready
- ✅ **Text Processing** - Automatic cleaning and tokenization

## 🛠️ Development

### Adding New Training Data
1. Add comment-reply pairs to `data/trainingdata/`
2. Format: `comment\treply\tstatus`
3. Run training: `python main.py train`

### Customizing Model
- Modify architecture in `model/model.py`
- Adjust parameters in training scripts
- Retrain with new configuration

### Extending Automation
- Update coordinates in `startytbot.py`
- Add new actions in bot workflow
- Customize popup interactions

## 🔍 Troubleshooting

### Common Issues

**Import Errors**
```bash
# For virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt

# For conda
conda activate yt-comment-reply-ai-bot
pip install -r requirements.txt
```

**GUI Not Starting**
```bash
# Install GUI dependencies
pip install customtkinter tkinter
```

**Model Loading Fails**
- Check if weight files exist in `data/`
- Verify tokenizer files are present
- Ensure model architecture matches weights

**Bot Automation Issues**
- Adjust screen coordinates for your display
- Check browser zoom level (should be 100%)
- Verify YouTube page layout matches expected

### Performance Tips
- **GPU Support**: Install CUDA for faster training
- **Memory Usage**: Reduce batch size if out of memory
- **Response Speed**: Use CPU for inference, GPU for training

## 📈 Model Performance

### Training Metrics
- **Loss Function**: Sparse categorical crossentropy
- **Optimizer**: Adam with default learning rate
- **Validation Split**: 80/20 train/validation
- **Early Stopping**: Based on validation loss

### Inference Speed
- **CPU**: ~200ms per comment
- **GPU**: ~50ms per comment
- **Memory**: ~2GB RAM usage

## 🤝 Contributing

### Adding Features
1. Fork the repository
2. Create feature branch
3. Implement changes
4. Test thoroughly
5. Submit pull request

### Training Data
- Contribute high-quality comment-reply pairs
- Ensure data is clean and relevant
- Follow existing format conventions

## 📄 License

This project is for educational and personal use. Ensure compliance with YouTube's Terms of Service when using automation features.

## ⚠️ Disclaimer

- **Automation Risk**: Use responsibly to avoid account restrictions
- **Rate Limiting**: Implement delays between actions
- **Manual Oversight**: Always review generated replies
- **Data Privacy**: Handle user data according to privacy laws