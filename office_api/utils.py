from evaluator.evaluate_contain import evaluate_contain

EVALUATION_FUNCTIONS = {
    "evaluate_contain": evaluate_contain
}

def run_evaluation(eval_spec):
    fn_name = eval_spec["function"]
    args = eval_spec["args"]

    if fn_name not in EVALUATION_FUNCTIONS:
        return {
            "success": False,
            "reason": "unknown_function"
        }

    return EVALUATION_FUNCTIONS[fn_name](**args)
