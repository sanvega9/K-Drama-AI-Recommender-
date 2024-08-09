import sys
from PyQt5.QtCore import Qt
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,QListWidget
from PyQt5.QtGui import QMovie, QFont
from PyQt5.QtCore import Qt
# Load the dataset K-Drama(Korean Drama)
kdrama = pd.read_csv('./K-Drama/kdrama.csv')

# Fill NaN values with empty strings
kdrama.fillna('',inplace= True)

#combine relevant features into a single strings
kdrama['combine_features']= (kdrama['Genre'] + ' '+ kdrama['Tags'] ).str.lower()

#Create TF-IDF Matrix
tfidf = TfidfVectorizer(stop_words='english')
matrixai = tfidf.fit_transform(kdrama['combine_features'])
#cosine similarity matrix
consine_sim = cosine_similarity(matrixai,matrixai)
#create a Sersie with indexai as titles 
indexai = pd.Series(kdrama.index, index=kdrama['Name'].str.lower()).drop_duplicates()
#recommendations
def get_recommendations(title, recommendations_number = 10):
    title = title.lower()
    if title not in indexai:
        return["K-Drama not found in the database."]
    idx = indexai[title]
    scores = list(enumerate(consine_sim[idx]))
    scores = sorted(scores,key=lambda x: x[1], reverse=True)
    scores = scores[1:recommendations_number + 1]
    kdramas_ai = [i[0]for i in scores]
    return kdrama['Name'].iloc[kdramas_ai].tolist()

def cast_name(title):
    if title in indexai:
        return kdrama.loc[indexai[title], 'Cast'].split(', ')
    else:
        return ["K-Drama not found in database."]
    
def actors_name(actor):
    kdramas_actor = kdrama[kdrama['Cast'].str.contains(actor, na= False)]
    return kdramas_actor ['Name'].tolist() if not kdramas_actor.empty else["Actor not found in database."]

class kdramaRecommenderAI(QWidget):
    def __init__(self):
        super().__init__()

        self.Appdesign()

    def Appdesign(self):
        self.setWindowTitle('AI K-Drama Recommender') 
        layoutai = QVBoxLayout()
        # Adding the background GIF
        self.backgroundai_label = QLabel(self)
        self.backgroundai_label.setGeometry(0,0,990,750)

        self.gifimage = QMovie("./K-Drama/kdrama.gif")
        self.backgroundai_label.setMovie(self.gifimage)
        self.gifimage.start()

        #user input the K-Drama Title 
        font = QFont('Times', 20, QFont.ExtraBold)
        font2 =  QFont('Times', 12, QFont.ExtraBold)
        self.lable = QLabel('Enter a K-Drama Title:') 
        self.lable.setFont(font)    
        self.lable.setStyleSheet('background-color: rgba(0, 50, 133, 0.8); color: #F3FEB8; padding: 10px; margin: 10px;')  # Light blue background with opacity, light yellow text, padding and margin
        self.lable.setAlignment(Qt.AlignCenter) 
        layoutai.addWidget(self.lable, alignment=Qt.AlignCenter)

    
        #create a transparent widget for content
        self.drama_txtbox_input = QLineEdit()
        self.drama_txtbox_input.setStyleSheet("QLineEdit { background-color: rgb(255, 255, 255, 0.7); }")
        layoutai.addWidget(self.drama_txtbox_input)

        self.buttonai = QPushButton('Get Recommendations')
        self.buttonai.clicked.connect(self.display_recommendations)
        layoutai.addWidget(self.buttonai)
        #kdrama recommendations 
        self.list_data  = QListWidget()
        self.list_data.setStyleSheet("QListWidget{ background-color: rgb(255, 255, 255, 0.7); }")
        layoutai.addWidget(self.list_data)
        #Cast label 
        self.castdisplay = QLabel('Cast:')
        self.castdisplay.setFont(font2)
        self.castdisplay.setStyleSheet('background-color: rgba(134, 10, 53, 0.7); color: #78DEC7; padding: 1px; margin: 10px;') 
         # Light blue background with opacity, light yellow text, padding and margin
        self.castdisplay.setAlignment(Qt.AlignCenter) 
        layoutai.addWidget(self.castdisplay,alignment=Qt.AlignCenter)
        #display the cast for the kdrama 
        self.cast_data  = QListWidget()
        self.cast_data.setStyleSheet("QListWidget{ background-color: rgb(255, 255, 255, 0.7); }")
        layoutai.addWidget(self.cast_data)
        #Actor name search up 
        self.actor_name = QLabel('Enter an Actor\'s name:')
        self.actor_name.setFont(font)
        self.actor_name.setStyleSheet('background-color: rgba(16, 68, 83, 0.7); color: #F36B6B; padding: 1px; margin: 10px;') 
        self.actor_name.setAlignment(Qt.AlignCenter) 
        layoutai.addWidget(self.actor_name,alignment=Qt.AlignCenter)

        self.actor_data  = QLineEdit()
        self.actor_data.setStyleSheet('QLineEdit { background-color: rgb(255, 255, 255, 0.7); }')
        layoutai.addWidget(self.actor_data)

        self.actor_button = QPushButton('Search for K-Dramas')
        layoutai.addWidget(self.actor_button)
        self.actor_button.clicked.connect(self.search_actor_kdrama)
        
        self.kdrama_list = QListWidget()
        self.kdrama_list.setStyleSheet("QListWidget{ background-color: rgba(255, 255, 255, 0.7)}")
        layoutai.addWidget(self.kdrama_list)

        self.setLayout(layoutai)

    def display_recommendations(self):
        title_name =self.drama_txtbox_input.text()
        recommendations = get_recommendations(title_name)

        self.list_data.clear()
        for drama in recommendations:
            self.list_data.addItem(drama)

        cast = cast_name(title_name)
        self.cast_data.clear()
        for actor in cast:
            self.cast_data.addItem(actor)

    def search_actor_kdrama(self):
        actor_data_name = self.actor_data.text()

        kdramas = actors_name(actor_data_name)
        self.kdrama_list.clear()
        for drama in kdramas:
            self.kdrama_list.addItem(drama)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    recommender = kdramaRecommenderAI()
    recommender.setGeometry(100, 100, 800, 750)#Abjust the window size view 
    recommender.show()
    sys.exit(app.exec_())