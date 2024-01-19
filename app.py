from flask import Flask, jsonify, render_template, request
import uuid

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True

lessons= []

#main page 
@app.route('/')
def index():
    return render_template('index.html')

# Create a new lesson
@app.route('/lessons', methods=['POST'])
def create_lesson():
    lesson_data = {
        'id': str(uuid.uuid4()),
        'title': request.form['title'],
        'description': request.form['description'],
        'type': request.form['type'],
        'impact': request.form['impact']
    }
    lessons.append(lesson_data)
    return jsonify({'message': 'Lesson created successfully'})

# Edit a lesson
@app.route('/lessons/<lesson_id>/edit', methods=['GET', 'POST'])
def edit_lesson(lesson_id):
    if request.method == 'GET':
        # Retrieve the lesson with the provided lesson_id from the database or list of lessons
        lesson = next((lesson for lesson in lessons if lesson['id'] == lesson_id), None)

        if lesson:
            # Render the edit form with the lesson data
            return render_template('edit_lesson.html', lesson=lesson)
        else:
            return jsonify({'error': 'Lesson not found'})

    elif request.method == 'POST':
        # Retrieve the updated lesson data from the form submitted in the request
        updated_data = request.form

        # Update the lesson with the provided lesson_id
        for lesson in lessons:
            if lesson['id'] == lesson_id:
                lesson.update(updated_data)
                break

        return jsonify({'message': 'Lesson updated successfully'})

# Get all lessons
@app.route('/lessons', methods=['GET'])
def get_lessons():
    # Your code to get all lessons goes here
    return render_template('lessons.html', lessons=lessons)

# Update a lesson
@app.route('/lessons/<id>', methods=['PUT'])
def update_lesson(id):
    for lesson in lessons:
        if lesson['id'] == id:
            lesson['title'] = request.form['title']
            lesson['description'] = request.form['description']
            lesson['type'] = request.form['type']
            lesson['impact'] = request.form['impact']
            return jsonify({'message': 'Lesson updated successfully'})
    return jsonify({'message': 'Lesson not found'})

# Delete a lesson
@app.route('/lessons/<lesson_id>/delete', methods=['DELETE', 'GET'])
def delete_lesson(lesson_id):
    # Find the lesson with the provided lesson_id
    lesson = next((lesson for lesson in lessons if lesson['id'] == lesson_id), None)

    if lesson:
        # Remove the lesson from the list
        lessons.remove(lesson)
        return jsonify({'message': 'Lesson deleted successfully'})
    else:
        return jsonify({'error': 'Lesson not found'})

if __name__ == '__main__':
    app.run()