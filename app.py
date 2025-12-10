import gradio as gr
import random

# Generate a random list of 8 unique integers between 1 and 50
def generateRandomList():
    arr = random.sample(range(1, 50), 8)
    return ",".join(map(str, arr))  # join into comma-separated string

# Display the array with cute colored boxes + arrow showing mid index
def highlightArray(arr, left, mid, right, target):
    html = ""
    for i, num in enumerate(arr):
        color = "#c7e2eb"  # default light blue each number box

        # mid index highlighted in pink
        if i == mid:
            color = "#facde0"

        # target number highlighted in green once found
        if num == target:
            color = "#c7ebcb"

        # mid index gets an arrow, others empty spacing
        arrow = "⤴︎" if i == mid else "&nbsp;"

        # HTML box formatting for UI
        html += f"""
        <div style='display:inline-block; width:45px; margin:3px; text-align:center;'>
            <div style='background:{color}; padding:8px; border-radius:6px; font-size:18px;'>{num}</div>
            <div style='font-size:20px'>{arrow}</div>
        </div>
        """
    return f"<div style='display:flex; justify-content:center;'>{html}</div>"

# Full binary search behind the scenes: returns both text + visuals for each step
def binarySearchSteps(arrayStr, target):
    # Handle invalid input such as letters, spaces, etc.
    try:
        arr = [int(x) for x in arrayStr.split(",")]
        target = int(target)
    except:
        return "enter valid integers!", []  # no visuals returned

    arr.sort()  # Binary search requires sorted array
    left, right = 0, len(arr) - 1

    # First instruction text
    stepsText = [f"⋆⭒˚.⋆ cat is searching for the mouse **{target}**! ⋆⭒˚.⋆\nsorted list: {arr}\n"]
    visuals = []

    # Main binary search loop
    while left <= right:
        mid = (left + right) // 2  # middle index

        visuals.append(highlightArray(arr, left, mid, right, target))
        stepsText.append(f"cat checks index {mid} → {arr[mid]}")

        # Target found
        if arr[mid] == target:
            stepsText.append(f"ᓚ₍ ^. .^₎ cat found the mouse at index **{mid}**!")
            visuals.append(highlightArray(arr, left, mid, right, target))
            return "\n".join(stepsText), visuals

        # Target located to the right half
        if arr[mid] < target:
            stepsText.append("mouse is on the RIGHT \n")
            left = mid + 1

        # Target located to the left half
        else:
            stepsText.append("mouse is on the LEFT \n")
            right = mid - 1

    # Out of loop means not found
    stepsText.append(f"no mouse! target **{target}** not found")
    return "\n".join(stepsText), visuals

# Handles clicking "next" to show steps one by one
def stepsThrough(arrStr, target, step):
    text, visuals = binarySearchSteps(arrStr, target)

    # If visuals exist, step forward through them
    if visuals:
        if step < len(visuals):
            return text, visuals[step], step + 1
        return text, visuals[-1], step  # if finished, stay
    return text, "", step

# Build GUI
with gr.Blocks() as demo:

    # Title with theme preserved
    gr.HTML("<h2 style='text-align:center;'>mouse chase! ≽(•⩊ •マ≼ → binary search</h2>")

    # User Inputs + Random Button
    with gr.Row():
        arrayIn = gr.Textbox(label="enter numbers (add commas) ⭑.ᐟ", placeholder="e.g. 5,2,8,9,1")
        targetIn = gr.Textbox(label="target ⭑.ᐟ", placeholder="e.g. 8")
        genBtn = gr.Button("random list ฅ^>⩊<^ฅ")

    # Connect random button to input textbox
    genBtn.click(generateRandomList, None, arrayIn)

    # Step tracking + UI outputs
    stepState = gr.State(0)
    outputText = gr.Textbox(label="cat’s clues ᓚ₍ ^. .^₎", lines=10)
    visOutput = gr.HTML()

    # Buttons for controlling search progress
    with gr.Row():
        startBtn = gr.Button("start / reset ᓚᘏᗢ")
        nextBtn = gr.Button("next ⋆˚꩜｡")

        # Start performs full search, returns results + reset step counter
        startBtn.click(
            lambda arr, t: (binarySearchSteps(arr, t)[0], "", 0),
            [arrayIn, targetIn],
            [outputText, visOutput, stepState]
        )

        # Next progresses step-by-step through visuals
        nextBtn.click(
            stepsThrough,
            [arrayIn, targetIn, stepState],
            [outputText, visOutput, stepState]
        )

# Launch the app
demo.launch()
