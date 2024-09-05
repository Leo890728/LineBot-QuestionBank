import random

from string import ascii_uppercase

from linebot.v3.messaging.models import (
    PostbackAction, 
    FlexText, 
    FlexBubble, 
    FlexBox, 
    FlexImage,
    FlexFiller,
    FlexBoxLinearGradient
)

from line_bot.utils.postback import QuestionPostback
from question_bank.models import (
    Question, Subject, Category, QuestionOption
)


class Template:

    @staticmethod
    def tag_bar(*tags) -> FlexBox:
        tag_box = FlexBox(
            layout="horizontal",
            position="absolute",
            spacing="5px",
            height="30px",
            width="90%",
            justify_content="flex-start",
            align_items="center",
            offset_start="5%",
            offset_top="2%",
            contents=[
                FlexBox(
                    layout="vertical",
                    background_color="#ff334b",
                    corner_radius="5px",
                    align_items="center",
                    contents=[
                        FlexText(
                            text=tag,
                            size="xs",
                            color="#ffffff",
                            align="center",
                            adjust_mode="shrink-to-fit",
                        )
                    ]
                )
            for tag in tags]
        )
        return tag_box

    @staticmethod
    def category_bubble(category: Category) -> FlexBubble:
        bubble = FlexBubble(
            body=FlexBox(
                padding_all="0px",
                layout="vertical",
                contents=[
                    FlexImage(
                        url=random.choice(category.background_image.split(";")),
                        gravity="center",
                        size="full",
                        aspect_ratio="1:1",
                        aspect_mode="cover",
                    ),
                    FlexBox(
                        layout="vertical",
                        position="absolute",
                        width="100%",
                        height="100%",
                        background=FlexBoxLinearGradient(
                            angle="0deg",
                            start_color="#00000099",
                            end_color="#00000000",
                        ),
                        contents=[],
                        action=PostbackAction(
                            text=category.name,
                            data=QuestionPostback.initialize(
                                flag=1, category_id=category.category_id)
                        )
                    ),
                    FlexBox(
                        layout="horizontal",
                        position="absolute",
                        padding_all="20px",
                        offset_end="0px",
                        offset_start="0px",
                        offset_bottom="0px",
                        contents=[
                            FlexText(
                                text=category.name,
                                color="#EEEEEE",
                                size="xxl"
                            )
                        ]
                    )
                ]
            )
        )
        return bubble

    @staticmethod
    def subject_bubble(subject: Subject, postback: QuestionPostback) -> FlexBubble:
        bubble = FlexBubble(
            body=FlexBox(
                layout='vertical',
                padding_all="0px",
                contents=[
                    FlexImage(
                        url=random.choice(subject.background_image.split(";")),
                        gravity="top",
                        size="full",
                        aspect_ratio="2:3",
                        aspect_mode="cover"
                    ),
                    # 背景暗化層
                    FlexBox(
                        layout='vertical',
                        position="absolute",
                        background_color="#2D2D2DAA",
                        offset_top="0px",
                        offset_bottom="0px",
                        offset_start="0px",
                        offset_end="0px",
                        padding_top="60px",
                        contents=[
                            Template.tag_bar(subject.name),
                            # 章節
                            FlexBox(
                                layout="vertical",
                                padding_start="5%",
                                padding_end="10%",
                                contents=[
                                    FlexText(
                                        text=subject.name,
                                        size="3xl",
                                        color="#ffffff",
                                        weight="regular",
                                        offset_top="0px",
                                    )
                                ]
                            ),
                            # 敘述
                            FlexBox(
                                layout="vertical",
                                margin="xxl",
                                padding_start="10%",
                                padding_end="10%",
                                contents=[
                                    FlexBox(
                                        layout="horizontal",
                                        spacing="lg",
                                        margin="xl",
                                        corner_radius="30px",
                                        contents=[
                                            FlexBox(
                                                layout="vertical",
                                                flex=0,
                                                contents=[
                                                    FlexFiller(),
                                                    FlexBox(
                                                        layout="vertical",
                                                        width="14px",
                                                        height="14px",
                                                        border_width="2px",
                                                        border_color="#ffffffcc",
                                                        corner_radius="30px",
                                                        contents=[
                                                            FlexFiller()
                                                        ]
                                                    ),
                                                    FlexFiller()
                                                ]
                                            ),
                                            FlexText(
                                                flex=4,
                                                text=desc,
                                                size="lg",
                                                gravity="center",
                                                color="#ffffffcc"
                                            )
                                        ]
                                    )
                                for desc in subject.description.split("\n")]
                            ),
                        ]
                    ),
                    FlexBox(
                        layout="horizontal",
                        position="absolute",
                        offset_bottom="15px",
                        offset_start="5%",
                        offset_end="5%",
                        contents=[
                            FlexBox(
                                layout='vertical',
                                height="40px",
                                border_width="1px",
                                border_color="#ffffff",
                                corner_radius="7px",
                                width="90%",
                                contents=[
                                    FlexFiller(),
                                    FlexBox(
                                        layout="baseline",
                                        spacing="sm",
                                        contents=[
                                            FlexText(
                                                text=f"共 {len(subject.questions)} 題",
                                                color="#ffffff",
                                                align="center",
                                                action=PostbackAction(
                                                    label="Test",
                                                    data=postback.configure(
                                                        flag=2,
                                                        subject_id=subject.subject_id
                                                    )
                                                )
                                            )
                                        ]
                                    ),
                                    FlexFiller()
                                ]
                            )
                        ]
                    )
                ]
            )
        )
        return bubble

    @staticmethod
    def mode_bubble(subject: Subject, postback: QuestionPostback) -> FlexBubble:
        bubble = FlexBubble(
            body=FlexBox(
                layout='vertical',
                padding_all="0px",
                height="200px",
                contents=[
                    FlexImage(
                        url=random.choice(subject.background_image.split(";")),
                        gravity="top",
                        size="full",
                        aspect_ratio="2:3",
                        aspect_mode="cover"
                    ),
                    # 背景暗化層
                    FlexBox(
                        layout='vertical',
                        position="absolute",
                        background_color="#2D2D2DAA",
                        offset_top="0px",
                        offset_bottom="0px",
                        offset_start="0px",
                        offset_end="0px",
                        padding_all="20px",
                        padding_top="135px",
                        contents=[
                            FlexBox(
                                layout="horizontal",
                                position="absolute",
                                offset_bottom="15px",
                                offset_start="15px",
                                offset_end="15px",
                                contents=[
                                    FlexBox(
                                        layout="vertical",
                                        spacing="sm",
                                        # margin = "xxl",
                                        height="40px",
                                        border_width="1px",
                                        border_color="#ffffff",
                                        corner_radius="4px",
                                        contents=[
                                            FlexFiller(),
                                            FlexBox(
                                                layout="baseline",
                                                spacing="sm",
                                                contents=[
                                                    FlexFiller(),
                                                    FlexText(
                                                        text="複習",
                                                        color="#ffffff",
                                                        offset_top="-2px",
                                                        action=PostbackAction(
                                                            data=postback.configure(
                                                                flag=3,
                                                                mode=QuestionPostback.QuestionModeType.REVISE,
                                                                question_seed=random.randint(0, 65535)
                                                            )
                                                        )
                                                    ),
                                                    FlexFiller()
                                                ]
                                            ),
                                            FlexFiller()
                                        ]
                                    ),
                                    FlexBox(
                                        layout="vertical",
                                        spacing="sm",
                                        margin="xl",
                                        height="40px",
                                        border_width="1px",
                                        border_color="#ffffff",
                                        corner_radius="4px",
                                        contents=[
                                            FlexFiller(),
                                            FlexBox(
                                                layout="baseline",
                                                spacing="sm",
                                                contents=[
                                                    FlexFiller(),
                                                    FlexText(
                                                        text="測驗",
                                                        color="#ffffff",
                                                        offset_top="-2px",
                                                        action=PostbackAction(
                                                            data=postback.configure(
                                                                flag=3,
                                                                mode=QuestionPostback.QuestionModeType.TEST,
                                                                question_seed=random.randint(0, 65535)
                                                            )
                                                        )
                                                    ),
                                                    FlexFiller()
                                                ]
                                            ),
                                            FlexFiller()
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    Template.tag_bar(subject.category.name, subject.name),
                    # 顯示題數
                    FlexBox(
                        layout="vertical",
                        position="absolute",
                        offset_top="30%",
                        offset_start="18px",
                        contents=[
                            FlexText(
                                text=f"{len(subject.questions)}題",
                                size="4xl",
                                color="#ffffff",
                                align="center"
                            )
                        ]
                    )
                ]
            )
        )
        return bubble

    @staticmethod
    def question_bubble(question: Question, postback: QuestionPostback)-> FlexBubble:

        question_index_tag = f"第{postback.question_index+1}/{len(question.subject.questions)}題"

        mode_tag = {QuestionPostback.QuestionModeType.REVISE: "複習", QuestionPostback.QuestionModeType.TEST: "測驗"}[postback.mode]

        def option_postback_action(question, option_index) -> PostbackAction:
            option = question.options[option_index]
            answers_id = [answer.option_id for answer in question.answer]
            reply_answer = postback.reply_answer

            if postback.mode == QuestionPostback.QuestionModeType.TEST:
                action_text = f"第{postback.question_index + 1}題 -> 選擇 {ascii_uppercase[option_index]}"

                if option.option_id in answers_id:
                    reply_answer += "*"
                else:
                    reply_answer += ascii_uppercase[option_index]

                postback_data = postback.configure(question_index=postback.question_index+1, reply_answer=reply_answer)

            elif postback.mode == QuestionPostback.QuestionModeType.REVISE:
                if option.option_id in answers_id:
                    action_text = f"第{postback.question_index + 1}題 -> {ascii_uppercase[option_index]} 正確"
                    postback_data = postback.configure(question_index=postback.question_index+1)
                else:
                    action_text = f"第{postback.question_index + 1}題 -> {ascii_uppercase[option_index]} 錯誤"
                    postback_data = " "

            return PostbackAction(text=action_text, data=postback_data) 


        bubble = FlexBubble(
            size="giga",
            body=FlexBox(
                layout="vertical",
                height="400px",
                padding_all="0px",
                contents=[
                    # 背景圖片
                    FlexImage(
                        url=random.choice(question.category.background_image.split(";")),
                        gravity="top",
                        size="full",
                        aspect_ratio="2:3.5",
                        aspect_mode="cover"
                    ),
                    # 背景暗化層
                    FlexBox(
                        layout="vertical",
                        position="absolute",
                        background_color="#000000cc",
                        offset_top="0px",
                        offset_bottom="0px",
                        offset_start="0px",
                        offset_end="0px",
                        padding_all="20px",
                        padding_top="20%",
                        contents=[
                            Template.tag_bar(
                                question.category.name, question.subject.name, mode_tag, question_index_tag),
                            # 題目
                            FlexBox(
                                layout="vertical",
                                contents=[
                                    FlexText(
                                        text=question.content,
                                        size="lg",
                                        color="#ffffff",
                                        weight="bold",
                                        wrap=True
                                    )
                                ]
                            ),
                            FlexBox(
                                layout="vertical",
                                spacing="sm",
                                margin="xl",
                                contents=[
                                    # 選項
                                    FlexBox(
                                        layout="baseline",
                                        spacing="lg",
                                        margin="xl" if option_index != 0 else "none",
                                        contents=[
                                            FlexText(
                                                text=f"{ascii_uppercase[option_index]}.",
                                                size="sm",
                                                flex=1,
                                                color="#ffffffcc",
                                            ),
                                            FlexText(
                                                text=option.content,
                                                size="sm",
                                                flex=18,
                                                color="#ffffffcc",
                                                wrap=True
                                            )
                                        ]
                                    )
                                    for option_index, option in enumerate(question.options)]
                            ),
                            # 選項按鈕
                            FlexBox(
                                layout="horizontal",
                                position="absolute",
                                offset_bottom="15px",
                                offset_start="15px",
                                offset_end="15px",
                                contents=[
                                    FlexBox(
                                        layout="vertical",
                                        margin="lg" if option_index != 0 else "none",
                                        height="40px",
                                        border_width="1px",
                                        border_color="#ffffff",
                                        corner_radius="5px",
                                        contents=[
                                            FlexFiller(),
                                            FlexBox(
                                                layout="baseline",
                                                spacing="sm",
                                                contents=[
                                                        FlexText(
                                                            text=ascii_uppercase[option_index],
                                                            size="xl",
                                                            color="#ffffff",
                                                            align="center",
                                                            action=option_postback_action(
                                                                question, option_index)
                                                        ),
                                                ]
                                            ),
                                            FlexFiller()
                                        ]
                                    )

                                    for option_index in range(len(question.options))
                                ]
                            )
                        ]
                    )
                ]
            )
        )
        # desc_bubble = FlexBubble(
        #     size="giga",
        #     body=FlexBox(
        #         layout="vertical",
        #         height="400px",
        #         padding_all="0px",
        #         contents=[
        #             # 背景圖片
        #             FlexImage(
        #                 url=random.choice(question.category.background_image.split(";")),
        #                 gravity="top",
        #                 size="full",
        #                 aspect_ratio="2:3.5",
        #                 aspect_mode="cover"
        #             ),
        #             # 背景暗化層
        #             FlexBox(
        #                 layout="vertical",
        #                 position="absolute",
        #                 background_color="#000000cc",
        #                 offset_top="0px",
        #                 offset_bottom="0px",
        #                 offset_start="0px",
        #                 offset_end="0px",
        #                 padding_all="20px",
        #                 padding_top="5%",
        #                 contents=[
        #                     FlexBox(
        #                         layout="vertical",
        #                         contents=[
        #                             FlexText(
        #                                 text="解析",
        #                                 size="xxl",
        #                                 color="#ffffff",
        #                                 weight="bold",
        #                                 wrap=True
        #                             ),
        #                             FlexText(
        #                                 text=question.desc,
        #                                 size="sm",
        #                                 margin="md",
        #                                 color="#ffffffcc",
        #                                 weight="bold",
        #                                 wrap=True
        #                             )
        #                         ]
        #                     )
        #                 ]
        #             )
        #         ]
        #     )
        # )
        # if postback.mode == QuestionPostback.QuestionModeType.REVISE and question.desc:
        #     return [bubble, desc_bubble]
        # else:
        #     return [bubble]
        return bubble

    @staticmethod
    def result_bubble(subject: Subject, postback: QuestionPostback) -> FlexBubble:

        mode_tag = {QuestionPostback.QuestionModeType.REVISE: "複習", QuestionPostback.QuestionModeType.TEST: "測驗"}[postback.mode]

        if postback.reply_answer:
            score = round((100 / len(subject.questions)) * QuestionPostback.ReplyAnswer.count_correct_answers(postback.reply_answer), 1)
        else:
            score = "None"

        bubble = FlexBubble(
            body=FlexBox(
                layout='vertical',
                padding_all="0px",
                height="200px",
                contents=[
                    FlexImage(
                        url=random.choice(subject.category.background_image.split(";")),
                        gravity="top",
                        size="full",
                        aspect_ratio="2:3",
                        aspect_mode="cover"
                    ),
                    FlexBox(
                        layout='vertical',
                        position="absolute",
                        background_color="#2D2D2DAA",
                        offset_top="0px",
                        offset_bottom="0px",
                        offset_start="0px",
                        offset_end="0px",
                        padding_all="20px",
                        padding_top="135px",
                        contents=[
                            FlexBox(
                                layout="horizontal",
                                contents=[
                                    # 按鍵
                                    FlexBox(
                                        layout="vertical",
                                        spacing="sm",
                                        # margin = "xxl",
                                        height="40px",
                                        border_width="1px",
                                        border_color="#ffffff",
                                        corner_radius="4px",
                                        contents=[
                                            FlexFiller(),
                                            FlexBox(
                                                layout="baseline",
                                                spacing="sm",
                                                contents=[
                                                    FlexText(
                                                        text=f"查看{QuestionPostback.ReplyAnswer.count_incorrect_answers(postback.reply_answer)}題錯誤",
                                                        color="#ffffff",
                                                        offset_top="-2px",
                                                        align="center",
                                                        action=PostbackAction(
                                                            text="查看錯誤 :P" if QuestionPostback.ReplyAnswer.count_incorrect_answers(
                                                                postback.reply_answer) else "沒有錯誤 :)",
                                                            data=postback.configure(flag=4, question_index=0) if QuestionPostback.ReplyAnswer.count_incorrect_answers(
                                                                postback.reply_answer) else " "
                                                        )
                                                    ) if postback.mode == QuestionPostback.QuestionModeType.TEST else
                                                    FlexText(
                                                        text="選擇其他科目",
                                                        color="#ffffff",
                                                        offset_top="-2px",
                                                        align="center",
                                                        action=PostbackAction(
                                                            data=QuestionPostback.initialize(
                                                                flag=1,
                                                                category_id=postback.category_id
                                                            )
                                                        )
                                                    )
                                                ]
                                            ),
                                            FlexFiller()
                                        ]
                                    ),
                                    FlexBox(
                                        layout="vertical",
                                        spacing="sm",
                                        margin="xl",
                                        height="40px",
                                        border_width="1px",
                                        border_color="#ffffff",
                                        corner_radius="4px",
                                        contents=[
                                            FlexFiller(),
                                            FlexBox(
                                                layout="baseline",
                                                spacing="sm",
                                                contents=[
                                                    FlexText(
                                                        text="重新測驗",
                                                        color="#ffffff",
                                                        offset_top="-2px",
                                                        align="center",
                                                        action=PostbackAction(
                                                            data=postback.configure(
                                                                flag=3,
                                                                question_index=0,
                                                                question_seed=random.randint(0, 65535),
                                                                reply_answer=""
                                                            )
                                                        )
                                                    ) if postback.mode == QuestionPostback.QuestionModeType.TEST else
                                                    FlexText(
                                                        text="重新複習",
                                                        color="#ffffff",
                                                        offset_top="-2px",
                                                        align="center",
                                                        action=PostbackAction(
                                                            data=postback.configure(
                                                                flag=3,
                                                                question_index=0,
                                                                question_seed=random.randint(0, 65535)
                                                            )
                                                        )
                                                    )
                                                ]
                                            ),
                                            FlexFiller(),
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    Template.tag_bar(subject.category.name, subject.name, mode_tag),
                    FlexBox(
                        layout="vertical",
                        position="absolute",
                        offset_top="30%",
                        offset_start="18px",
                        contents=[
                            FlexText(
                                text=f"{score}分" if postback.reply_answer else "結束",
                                size="4xl",
                                color="#ffffff",
                                align="center",
                            )
                        ]
                    )
                ]
            )
        )
        return bubble

    @staticmethod
    def review_bubble(question: Question, question_index: int, prev_question_index: int, next_question_index: int, postback: QuestionPostback) -> FlexBubble:

        def option_background_color(option: QuestionOption, option_index: int) -> str:
            if option.option_id in [answer.option_id for answer in question.answer]:
                result = "#13C900cc"
            elif ascii_uppercase[option_index] == postback.reply_answer[question_index]:
                result = "#FF2D2Dcc"
            else:
                result = None
            return result

        question_index_tag = "第{0}/{1}題".format(
            question_index+1, len(question.subject.questions))

        bubble = FlexBubble(
            size="giga",
            body=FlexBox(
                layout="vertical",
                height="400px",
                padding_all="0px",
                contents=[
                    # 背景圖片
                    FlexImage(
                        url=random.choice(question.category.background_image.split(";")),
                        gravity="top",
                        size="full",
                        aspect_ratio="2:3.5",
                        aspect_mode="cover"
                    ),
                    # 背景暗化層
                    FlexBox(
                        layout="vertical",
                        position="absolute",
                        background_color="#000000cc",
                        offset_top="0px",
                        offset_bottom="0px",
                        offset_start="0px",
                        offset_end="0px",
                        padding_all="20px",
                        padding_top="20%",
                        contents=[
                            Template.tag_bar(
                                question.category.name, question.subject.name, "查看", question_index_tag),
                            # 題目
                            FlexBox(
                                layout="vertical",
                                contents=[
                                    FlexText(
                                        text=question.content,
                                        size="lg",
                                        color="#ffffff",
                                        weight="bold",
                                        wrap=True
                                    )
                                ]
                            ),
                            # 選項
                            FlexBox(
                                layout="vertical",
                                spacing="sm",
                                margin="xl",
                                contents=[
                                    FlexBox(
                                        layout="baseline",
                                        spacing="xs",
                                        corner_radius="5px",
                                        margin="lg" if option_index != 0 else "none",
                                        background_color=option_background_color(
                                            option, option_index),
                                        contents=[
                                            FlexText(
                                                text=f" {ascii_uppercase[option_index]}.",
                                                size="sm",
                                                flex=1,
                                                color="#ffffffcc",
                                            ),
                                            FlexText(
                                                text=str(option.content),
                                                size="sm",
                                                flex=10,
                                                color="#ffffffcc",
                                                wrap=True
                                            )
                                        ]
                                    )
                                    for option_index, option in enumerate(question.options)]
                            ),
                            # 選項按鈕
                            FlexBox(
                                layout="horizontal",
                                position="absolute",
                                offset_bottom="15px",
                                offset_start="10px",
                                offset_end="10px",
                                contents=[
                                    FlexBox(
                                        layout="vertical",
                                        # margin = "xl",
                                        height="40px",
                                        border_width="1px",
                                        border_color="#ffffff",
                                        corner_radius="4px",
                                        contents=[
                                            FlexFiller(),
                                            FlexBox(
                                                layout="baseline",
                                                spacing="sm",
                                                contents=[
                                                    FlexFiller(),
                                                    FlexText(
                                                        text=f"第{prev_question_index+1}題",
                                                        color="#ffffff",
                                                        flex=0,
                                                        action=PostbackAction(
                                                            text=f"上一題 -> 第{prev_question_index+1}題",
                                                            data=postback.configure(
                                                                question_index=prev_question_index
                                                            )
                                                        )
                                                    ),
                                                    FlexFiller()
                                                ]
                                            ),
                                            FlexFiller()
                                        ]
                                    ),
                                    FlexBox(
                                        layout="vertical",
                                        # margin = "xl",
                                        height="40px",
                                        border_width="1px",
                                        corner_radius="4px",
                                        contents=[
                                            FlexFiller(),
                                            FlexBox(
                                                layout="baseline",
                                                spacing="sm",
                                                contents=[
                                                    FlexFiller(),
                                                    FlexText(
                                                        text="◈",
                                                        color="#ffffff",
                                                        action=PostbackAction(
                                                            data=QuestionPostback.initialize()
                                                        )
                                                    )
                                                ]
                                            ),
                                            FlexFiller()
                                        ]
                                    ),
                                    FlexBox(
                                        layout="vertical",
                                        margin="xl",
                                        height="40px",
                                        border_width="1px",
                                        border_color="#ffffff",
                                        corner_radius="4px",
                                        contents=[
                                            FlexFiller(),
                                            FlexBox(
                                                layout="baseline",
                                                spacing="sm",
                                                contents=[
                                                    FlexFiller(),
                                                    FlexText(
                                                        text=f"第{next_question_index+1}題",
                                                        color="#ffffff",
                                                        flex=0,
                                                        action=PostbackAction(
                                                            text=f"下一題 -> 第{next_question_index+1}題",
                                                            data=postback.configure(
                                                                question_index=next_question_index
                                                            )
                                                        )
                                                    ),
                                                    FlexFiller()
                                                ]
                                            ),
                                            FlexFiller()
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        )
        return bubble
