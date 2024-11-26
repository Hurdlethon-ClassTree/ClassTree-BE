from ..models import User
from rest_framework import serializers
from hurdlethon.models import Lecture


class MypageUpdateSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        lectures = Lecture.objects.all()
        choices = [(lecture.lecture_id, lecture.lecture_name) for lecture in lectures]
        lecture_count = Lecture.objects.count()
        max_fields = min(lecture_count, 10)  # 최대 10개의 필드 생성

        # 동적으로 관심 강의 필드 추가
        for i in range(max_fields):
            self.fields[f'interest_{i + 1}'] = serializers.ChoiceField(
                choices=choices,
                required=False,
                allow_null=True,
                help_text=f"Select Lecture for interest {i + 1}",
            )

    class Meta:
        model = User
        fields = ['nickname', 'major', 'school_email', 'student_number']

    def update(self,instance, validated_data):
        # 관심 강의 필드 데이터 수집
        lecture_ids = []
        for i in range(10):
            key = f'interest_{i + 1}'
            if key in validated_data:
                value = validated_data.pop(key)
                if value is not None:
                    lecture_ids.append(value)
        #중복 체크
        if len(lecture_ids) != len(set(lecture_ids)):
            raise serializers.ValidationError("Duplicate lecture IDs are not allowed.")

        # 강의 유효성 검사
        invalid_ids = [id for id in lecture_ids if not Lecture.objects.filter(lecture_id=id).exists()]
        if invalid_ids:
            raise serializers.ValidationError(f"Invalid Lecture IDs: {invalid_ids}")

        # 관심 강의 저장
        instance.interests = lecture_ids

        #나머지 필드 업데이트
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance