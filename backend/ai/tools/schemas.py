get_chat_details_tool_schema = {
    "name": "get_chat_details",
    "description": "Fetch the chat_details of a Chat. No input parameters required from the LLM.",
    "parameters": {
        "type": "object",
        "properties": {},
        "additionalProperties": False
    }
}

get_user_details_tool_schema = {
    "name": "get_user_details",
    "description": "Fetch the user_details of a User. No input parameters required from the LLM.",
    "parameters": {
        "type": "object",
        "properties": {},
        "additionalProperties": False
    }
}

update_chat_details_tool_schema = {
  "name": "update_chat_details",
  "description": "Update a Chat's chat_details. Supports string fields, list operations, and dict updates.",
  "parameters": {
    "type": "object",
    "properties": {
      "updates": {
        "type": "object",
        "description": "Fields to update in chat_details.",
        "properties": {
          "current_mood": {"type": "string"},
          "nickname": {"type": "string"},
          "rules": {
            "type": "object",
            "properties": {
              "add": {"type": ["string", "array"], "items": {"type": "string"}},
              "remove": {"type": ["string", "array"], "items": {"type": "string"}}
            }
          },
          "important_events": {
            "type": "object",
            "properties": {
              "add": {"type": ["string", "array"], "items": {"type": "string"}},
              "remove": {"type": ["string", "array"], "items": {"type": "string"}}
            }
          },
          "any_other_such_details": {
            "type": "object",
            "properties": {
              "set": {"type": "object", "additionalProperties": true},
              "remove": {"type": ["string", "array"], "items": {"type": "string"}}
            }
          }
        },
        "additionalProperties": false
      }
    },
    "required": ["updates"]
  }
}

update_user_details_tool_schema = {
    update_user_details_tool = {
        "name": "update_user_details",
        "description": "Update fields in a User's user_details.",
        "parameters": {
            "type": "object",
            "properties": {
                "updates": {
                    "type": "object",
                    "description": "Fields to update in user_details.",
                    "properties": {
                        "nickname": {"type": "string"},
                        "available_timings": {"type": "string"},
                        "preferences": {
                            "type": "object",
                            "properties": {
                                "add": {
                                    "type": ["string", "array"],
                                    "items": {"type": "string"}
                                },
                                "remove": {
                                    "type": ["string", "array"],
                                    "items": {"type": "string"}
                                }
                            },
                            "additionalProperties": False
                        },
                        "dislikes": {
                            "type": "object",
                            "properties": {
                                "add": {
                                    "type": ["string", "array"],
                                    "items": {"type": "string"}
                                },
                                "remove": {
                                    "type": ["string", "array"],
                                    "items": {"type": "string"}
                                }
                            },
                            "additionalProperties": False
                        },
                        "task_following_record": {
                            "type": "object",
                            "properties": {
                                "add": {
                                    "type": ["string", "array"],
                                    "items": {"type": "string"}
                                },
                                "remove": {
                                    "type": ["string", "array"],
                                    "items": {"type": "string"}
                                }
                            },
                            "additionalProperties": False
                        }
                        "anything_else": {
                            "type": "object",
                            "properties": {
                                "add": {
                                    "type": ["string", "array"],
                                    "items": {"type": "string"}
                                },
                                "remove": {
                                    "type": ["string", "array"],
                                    "items": {"type": "string"}
                                }
                            },
                            "additionalProperties": False
                        }
                    },
                    "additionalProperties": False
                }
            },
            "required": ["updates"]
        }
    }
}

clear_chat_details_tool_schema = {
    "name": "clear_chat_details",
    "description": "Resets the chat_details of a Chat to an empty ChatDetails object. No input parameters required from the LLM.",
    "parameters": {
        "type": "object",
        "properties": {},
        "additionalProperties": False
    }
}

clear_user_details_tool_schema = {
    "name": "clear_user_details",
    "description": "Resets the user_details of a User to an empty UserDetails object. No input parameters required from the LLM.",
    "parameters": {
        "type": "object",
        "properties": {},
        "additionalProperties": False
    }
}