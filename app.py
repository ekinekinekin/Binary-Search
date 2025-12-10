import gradio as gr
import random

def generateRandomList():
    arr = random.sample(range(1, 50), 8)
    return ",".join(map(str, arr))

def highlightArray(arr, left, mid, right, target):
    html = ""
    for i, num in enumerate(arr):
        color = "#c7e2eb"  # light blue

        if i == mid:
            color = "#facde0"  # pink
        if num == target:
            color = "#c7ebcb"  # green

        arrow = "⤴︎" if i == mid else "&nbsp;"
        html += f"""
        <div style='display:inline-block; width:45px; margin:3px; text-align:center;'>
            <div style='background:{color}; padding:8px; border-radius:6px; font-size:18px;'>{num}</div>
            <div style='font-size:20px'>{arrow}</div>
        </div>
        """
    return f"<div style='display:flex; justify-content:center;'>{html}</div>"

def binarySearchSteps(arrayStr, target):
    try:
        arr = [int(x) for x in arrayStr.split(",")]
        target = int(target)
    except:
        return "enter valid integers!", []

    arr.sort()
    left, right = 0, len(arr) - 1
    stepsText = [f"⋆⭒˚.⋆ cat is searching for the mouse **{target}**! ⋆⭒˚.⋆\nsorted list: {arr}\n"]
    visuals = []

    while left <= right:
        mid = (left + right) // 2

        visuals.append(highlightArray(arr, left, mid, right, target))
        stepsText.append(f"cat checks index {mid} → {arr[mid]}")

        if arr[mid] == target:
            stepsText.append(f"ᓚ₍ ^. .^₎ cat found the mouse at index **{mid}**!")
            visuals.append(highlightArray(arr, left, mid, right, target))
            return "\n".join(stepsText), visuals

        if arr[mid] < target:
            stepsText.append("mouse is on the RIGHT ➡️\n")
            left = mid + 1
        else:
            stepsText.append("mouse is on the LEFT ⬅️\n")
            right = mid - 1

    stepsText.append(f"no mouse ｡ﾟ(｡ﾉωヽ｡)ﾟ｡ target **{target}** not found")
    return "\n".join(stepsText), visuals

def stepsThrough(arrStr, target, step):
    text, visuals = binarySearchSteps(arrStr, target)
    if visuals:
        if step < len(visuals):
            return text, visuals[step], step + 1
        return text, visuals[-1], step
    return text, "", step

with gr.Blocks() as demo:

    gr.HTML("<h2 style='text-align:center;'>mouse chase! ≽(•⩊ •マ≼ → binary search</h2>")

    with gr.Row():
        arrayIn = gr.Textbox(label="enter numbers (add commas) ⭑.ᐟ", placeholder="e.g. 5,2,8,9,1")
        targetIn = gr.Textbox(label="target ⭑.ᐟ", placeholder="e.g. 8")
        genBtn = gr.Button("random list ฅ^>⩊<^ฅ")

    genBtn.click(generateRandomList, None, arrayIn)

    stepState = gr.State(0)
    outputText = gr.Textbox(label="cat’s clues ᓚ₍ ^. .^₎", lines=10)
    visOutput = gr.HTML()

    with gr.Row():
        startBtn = gr.Button("start / reset ᓚᘏᗢ")
        nextBtn = gr.Button("next ⋆˚꩜｡")

        startBtn.click(
            lambda arr, t: (binarySearchSteps(arr, t)[0], "", 0),
            [arrayIn, targetIn],
            [outputText, visOutput, stepState]
        )

        nextBtn.click(
            stepsThrough,
            [arrayIn, targetIn, stepState],
            [outputText, visOutput, stepState]
        )

demo.launch()
