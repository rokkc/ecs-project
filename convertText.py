from flask import Flask, send_file, request
from PIL import Image
from PIL import ImageEnhance

app = Flask(__name__)


@app.route("/")
def myform():
    form_file = '/Users/yash/PycharmProject/flaskServer/resources/form.html'
    return send_file(form_file, mimetype='text/html')

@app.route("/output.html")
def myoutput():
    output_file = '/Users/yash/PycharmProject/flaskServer/resources/output.html'
    return send_file(output_file, mimetype='text/html')


@app.route("/image.png")
def myimage():
    image_file = '/tmp/handwriting_image.png'
    return send_file(image_file, mimetype='image/png')


@app.route('/handwriting')
def myapp():
    if request.method == 'GET':
        textToHandwriting(request.args['text'])
        #new_image_file = '/Users/yash/handwritingProject/sample.png'
        #return send_file(new_image_file, mimetype='image/png')
        output_file = '/Users/yash/PycharmProject/flaskServer/resources/output.html'
        return send_file(output_file, mimetype='text/html')


def textToHandwriting(letters):
    # Set starting coordinates for text
    xstart = 140
    ystart = 175

    # Open an image from the user's computer
    image = Image.open('/Users/yash/PycharmProject/textToHandwritingReal/binderPaper.png')

    # Enhance the brightness of the image
    image_brightness = ImageEnhance.Brightness(image)
    bright_image = image_brightness.enhance(0.65)
    image = bright_image.copy()

    # Set initial x and y coordinates for text placement
    y = ystart
    x = xstart

    i = 1
    for letter in letters:
        # Open an image of the current letter from the user's computer
        image_to_paste = Image.open('/Users/yash/PycharmProject/textToHandwritingReal/Letters/' + str(letter) + '.png')

        # Enhance the brightness of the letter image
        image_to_paste_brightness = ImageEnhance.Brightness(image_to_paste)
        bright_image_to_paste = image_to_paste_brightness.enhance(0.9)

        # Resize the letter image to half its original size
        size_factor = 0.5
        new_width = int(bright_image_to_paste.width * size_factor)
        new_height = int(bright_image_to_paste.height * size_factor)
        resized_image = bright_image_to_paste.resize((new_width, new_height), Image.LANCZOS)

        # Paste the letter onto the main image at the current x and y coordinates
        image.alpha_composite(resized_image, (x, y))

        # Update x and y coordinates for next letter placement
        if x > 760:
            x = xstart
            y += 33

            if i > 30:
                # Show current page and start a new page if more than 30 lines have been written
                image.show()
                image = bright_image.copy()
                x = xstart
                y = ystart

                i = 0

            if i % 6 == 0:
                y -= 2

            i += 1

        else:
            if letter == ' ':
                x += 27


            else:
                x += 13

    # Display final page of text
    new_image_file = '/tmp/handwriting_image.png'
    image.save(new_image_file)


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8080)

